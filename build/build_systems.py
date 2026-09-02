#!/usr/bin/env python3
"""Build [Ln(OH)3(H2O)n] + bulk water systems as periodic boxes and free droplets.

Every system has the same composition::

    Ln(3+)  +  3 OH(-)  +  128 H2O      ->  391 atoms, net charge 0

Four boundary-condition variants are produced per lanthanide:

    box_pbc        cube at liquid-water density, fully periodic
    box_nonpbc     identical coordinates, treated as a finite cube-shaped cluster
    droplet_pbc    spherical droplet centred in a large vacuum cell
    droplet_nonpbc identical droplet, no cell at all

box_pbc / box_nonpbc share Cartesian coordinates exactly, and droplet_pbc /
droplet_nonpbc differ only by a rigid translation, so the pbc vs non-pbc
comparison is a pure boundary-condition test at fixed geometry.

Construction is a two-stage process.  Stage A fixes every oxygen position: the
first coordination shell is built from ideal tricapped-trigonal-prism (CN 9) or
square-antiprism (CN 8) geometry, and the bulk oxygens are relaxed from a random
start by iterative pair separation until no O-O contact is shorter than the
target.  Stage B adds hydrogens, choosing each molecule's orientation to
minimise a soft steric penalty against everything placed so far.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation

from ln_data import (
    ANGLE_HOH,
    ANGLE_LN_O_H,
    LN_DATA,
    MIN_HH_INTER,
    MIN_LN_O_BULK,
    MIN_OH_INTER,
    MIN_OO_SHELL,
    NET_CHARGE,
    N_HYDROXIDE,
    N_WATER,
    R_OH_HYDROXIDE,
    R_OH_WATER,
    RHO_WATER_MASS,
    RHO_WATER_NUM,
)

# Vacuum gap between periodic images of a droplet.  Must exceed the largest
# receptive field among the target models (MACE-POLAR-1-L: 18 A).
VACUUM_GAP = 22.0

TTP_PRISM_POLAR = 48.0  # deg from the C3 axis, [Ln(H2O)9]3+ tricapped trig. prism
SAP_POLAR = 59.25  # deg from the C4 axis, ideal square antiprism

OO_TARGET = 2.72  # A, separation enforced during the bulk oxygen relaxation
N_TRIAL = 160  # orientations screened per molecule
N_SWEEP = 8  # refinement passes over all molecular orientations

# Soft targets used by the orientation search.  They sit above the acceptance
# thresholds in ln_data so that the accepted structures keep some margin.
PEN_OO = MIN_OO_SHELL + 0.05
PEN_OH = MIN_OH_INTER + 0.12
PEN_HH = MIN_HH_INTER + 0.15

# Orientation objective: hard-sphere overlap is weighted so that violating a
# soft target by ~0.15 A always costs more than the two hydrogen bonds a water
# can donate, i.e. sterics can never be traded away for H-bonding.
W_STERIC = 100.0
W_HBOND = 0.8
HB_R0, HB_WIDTH = 1.90, 0.30  # A, optimum and width of the O...H reward
HB_COS_ONSET = 0.5  # reward starts once cos(O-H...O) < -0.5 (angle > 120 deg)


# --------------------------------------------------------------------------- #
# small geometry helpers
# --------------------------------------------------------------------------- #
def unit(v):
    return v / np.linalg.norm(v)


def perp_frame(u):
    """Two unit vectors completing a right-handed frame with `u`."""
    seed = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(seed, u)) > 0.9:
        seed = np.array([1.0, 0.0, 0.0])
    v = unit(seed - np.dot(seed, u) * u)
    return v, np.cross(u, v)


def random_rotations(rng, n):
    """Uniformly distributed rotations, via normalised random quaternions."""
    q = rng.normal(size=(n, 4))
    q /= np.linalg.norm(q, axis=1)[:, None]
    return Rotation.from_quat(q)


def spherical_dir(polar_deg, azim_deg):
    t, p = np.radians(polar_deg), np.radians(azim_deg)
    return np.array([np.sin(t) * np.cos(p), np.sin(t) * np.sin(p), np.cos(t)])


def shell_site_dirs(cn):
    """Unit vectors of the ideal CN-9 (TTP) or CN-8 (SAP) coordination polyhedron."""
    if cn == 9:
        dirs = [spherical_dir(90.0, a) for a in (0.0, 120.0, 240.0)]  # caps
        for az in (60.0, 180.0, 300.0):  # eclipsed trigonal prism
            dirs.append(spherical_dir(TTP_PRISM_POLAR, az))
            dirs.append(spherical_dir(180.0 - TTP_PRISM_POLAR, az))
        return dirs
    if cn == 8:
        dirs = [spherical_dir(SAP_POLAR, a) for a in (0.0, 90.0, 180.0, 270.0)]
        dirs += [spherical_dir(180.0 - SAP_POLAR, a) for a in (45.0, 135.0, 225.0, 315.0)]
        return dirs
    raise ValueError(f"unsupported coordination number {cn}")


def water_hydrogens(o_pos, u_out, azim):
    """H positions of a water whose HOH bisector points along `u_out`.

    For a coordinated water `u_out` is the Ln->O direction, which puts the
    dipole pointing away from the cation and the lone pairs towards it.
    """
    v, w = perp_frame(u_out)
    azim = np.atleast_1d(azim)[:, None]
    e = np.cos(azim) * v + np.sin(azim) * w
    half = np.radians(ANGLE_HOH / 2.0)
    par = R_OH_WATER * np.cos(half) * u_out
    perp = R_OH_WATER * np.sin(half) * e
    return np.stack([o_pos + par + perp, o_pos + par - perp], axis=1)


def hydroxide_hydrogen(o_pos, u_out, azim):
    """H position of a coordinated OH-, tilted ANGLE_LN_O_H at the oxygen."""
    v, w = perp_frame(u_out)
    azim = np.atleast_1d(azim)[:, None]
    e = np.cos(azim) * v + np.sin(azim) * w
    tilt = np.radians(180.0 - ANGLE_LN_O_H)  # angle between O->H and Ln->O
    return o_pos + R_OH_HYDROXIDE * (np.cos(tilt) * u_out + np.sin(tilt) * e)


def free_water_hydrogens(o_pos, rots):
    """H positions of `len(rots)` randomly oriented waters on the same oxygen."""
    half = np.radians(ANGLE_HOH / 2.0)
    template = R_OH_WATER * np.array(
        [[np.cos(half), np.sin(half), 0.0], [np.cos(half), -np.sin(half), 0.0]]
    )
    return o_pos + np.stack([r.apply(template) for r in rots])


# --------------------------------------------------------------------------- #
# stage A: oxygen skeleton
# --------------------------------------------------------------------------- #
def choose_hydroxide_sites(dirs, d_oh, n_oh=N_HYDROXIDE):
    """Pick the n_oh shell sites whose mutual separation is largest.

    Hydroxides are anions and repel one another, so of all the ways to put three
    OH- in the first shell the maximally separated arrangement is the sensible
    starting guess.  For CN 9 this always selects the three equatorial caps.
    """
    best, best_score = None, -np.inf
    for combo in itertools.combinations(range(len(dirs)), n_oh):
        pos = np.array([dirs[i] * d_oh for i in combo])
        d = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=-1)
        score = d[np.triu_indices(n_oh, 1)].min()
        if score > best_score:
            best, best_score = combo, score
    return list(best), best_score


def build_shell(sym, ln_pos, rng):
    """First-shell oxygen positions (hydroxide and water) about `ln_pos`."""
    info = LN_DATA[sym]
    dirs = shell_site_dirs(info["cn"])
    oh_idx, oh_sep = choose_hydroxide_sites(dirs, info["d_oh"])

    rot = random_rotations(rng, 1)[0]
    dirs = [rot.apply(d) for d in dirs]

    oh_o = np.array([ln_pos + d * info["d_oh"] for i, d in enumerate(dirs) if i in oh_idx])
    wat_o = np.array(
        [ln_pos + d * info["d_ow"] for i, d in enumerate(dirs) if i not in oh_idx]
    )
    return oh_o, wat_o, oh_sep


def relax_bulk_oxygens(
    fixed, movable, ln_pos, *, cell=None, radius=None, n_iter=2000, rng=None
):
    """Push `movable` oxygens apart until every O-O contact clears OO_TARGET.

    `fixed` holds the first-shell oxygens, which never move: their mutual
    distances are set by the coordination polyhedron and are legitimately
    shorter than OO_TARGET, so fixed-fixed pairs are excluded from both the
    displacements and the convergence test.  Confinement is either a periodic
    cube of edge `cell` or a hard sphere of `radius` centred on `ln_pos`.
    """
    movable = movable.copy()
    n_fix = len(fixed)
    it = 0

    for it in range(n_iter):
        pts = np.vstack([fixed, movable])
        tree = (
            cKDTree(np.mod(pts, cell), boxsize=cell) if cell is not None else cKDTree(pts)
        )
        pairs = tree.query_pairs(OO_TARGET, output_type="ndarray")
        if len(pairs):  # a rigid pair cannot be relaxed, so ignore it
            pairs = pairs[(pairs >= n_fix).any(axis=1)]

        disp = np.zeros_like(pts)
        worst = 0.0
        if len(pairs):
            d_vec = pts[pairs[:, 1]] - pts[pairs[:, 0]]
            if cell is not None:
                d_vec -= cell * np.round(d_vec / cell)
            dist = np.maximum(np.linalg.norm(d_vec, axis=1), 1e-6)
            deficit = OO_TARGET - dist
            worst = float(deficit.max())
            step = 0.55 * (deficit / dist)[:, None] * d_vec
            np.add.at(disp, pairs[:, 0], -step)
            np.add.at(disp, pairs[:, 1], step)

        # keep bulk oxygens out of the first coordination shell
        if ln_pos is not None:
            rel = movable - ln_pos
            if cell is not None:
                rel -= cell * np.round(rel / cell)
            r = np.maximum(np.linalg.norm(rel, axis=1), 1e-6)
            close = r < MIN_LN_O_BULK
            if close.any():
                worst = max(worst, float((MIN_LN_O_BULK - r[close]).max()))
                disp[n_fix:][close] += (
                    ((MIN_LN_O_BULK - r[close]) / r[close])[:, None] * rel[close]
                )

        movable += disp[n_fix:]

        if radius is not None:  # pull escapees back inside the droplet
            rel = movable - ln_pos
            r = np.linalg.norm(rel, axis=1)
            out = r > radius
            if out.any():
                movable[out] = ln_pos + rel[out] * (radius / r[out])[:, None]
        if cell is not None:
            movable = np.mod(movable, cell)

        if worst < 1e-3:
            break
        if rng is not None and it % 300 == 299 and worst > 0.05:
            movable += rng.normal(scale=0.02, size=movable.shape)  # unjam

    return movable, it + 1, worst


CAVITY_TARGET = 3.0  # A, tolerated radius of the largest oxygen-free sphere
CAVITY_SPACING = 0.35  # A, probe grid resolution


def cavity_scan(o_pos, *, cell=None, centre=None, r_in=None, spacing=CAVITY_SPACING):
    """Characterise the oxygen-free space in a region.

    Returns (largest cavity radius, its centre, total excess void volume).  For
    a periodic cube pass `cell`; for a cluster pass `centre` and `r_in` so that
    only the interior is probed and the surrounding vacuum is not mistaken for a
    cavity.  An ideal lattice at liquid-water density has a largest interstitial
    of about 2.5 A, so anything much above 3 A is a real void.

    The excess volume aggregates *all* oversized cavities, not just the worst
    one.  Optimising the maximum alone stalls on plateaus, because relocating a
    molecule often has to reshape several cavities before the largest shrinks.
    """
    if cell is not None:
        axes = [np.arange(0.0, cell, spacing)] * 3
        grid = np.stack(np.meshgrid(*axes, indexing="ij"), -1).reshape(-1, 3)
        tree = cKDTree(np.mod(o_pos, cell), boxsize=cell)
        dist, _ = tree.query(np.mod(grid, cell))
    else:
        axes = [np.arange(-r_in, r_in + spacing, spacing)] * 3
        grid = centre + np.stack(np.meshgrid(*axes, indexing="ij"), -1).reshape(-1, 3)
        grid = grid[np.linalg.norm(grid - centre, axis=1) <= r_in]
        dist, _ = cKDTree(o_pos).query(grid)
    k = int(np.argmax(dist))
    excess = float((np.maximum(0.0, dist - CAVITY_TARGET) ** 3).sum()) * spacing**3
    return float(dist[k]), grid[k], excess


def fill_voids(
    fixed, movable, ln_pos, *, cell=None, radius=None, rng, max_moves=300, margin=1.7
):
    """Even out the local density by moving crowded oxygens into voids.

    The pairwise relaxation only resolves overlaps locally, so it leaves
    mesoscale density fluctuations: regions dense enough to open a hole large
    enough for another water elsewhere.  Each step relocates the most crowded
    movable oxygen into the largest cavity and re-relaxes; the move is kept only
    if the largest cavity actually shrank, so the metric improves monotonically.
    """
    def worst_cavity(mov):
        o = np.vstack([fixed, mov])
        if cell is not None:
            return cavity_scan(o, cell=cell)
        # the droplet surface is free, so the probe region tracks its extent
        r_in = np.linalg.norm(o - ln_pos, axis=1).max() - margin
        return cavity_scan(o, centre=ln_pos, r_in=r_in)

    best_r, best_pt, best_excess = worst_cavity(movable)
    n_moves = 0
    for _ in range(max_moves):
        if best_r <= CAVITY_TARGET:
            break
        # crowding measure: distance to the 4th nearest oxygen
        pts = np.vstack([fixed, movable])
        dist, _ = cKDTree(pts).query(movable, k=5)
        crowded = np.argsort(dist[:, 4])[:20]
        # A crowded donor is the cheapest to move, but relocating it does not
        # always shrink the worst cavity, so random donors are tried as well.
        pool = np.concatenate([crowded, rng.choice(len(movable), 20, replace=False)])

        improved = False
        for cand in pool:
            trial = movable.copy()
            trial[cand] = best_pt + rng.normal(scale=0.05, size=3)
            trial, _, _ = relax_bulk_oxygens(
                fixed, trial, ln_pos, cell=cell, radius=radius, n_iter=400
            )
            r, pt, excess = worst_cavity(trial)
            if excess < best_excess * (1.0 - 1e-3):
                movable, best_r, best_pt, best_excess = trial, r, pt, excess
                improved = True
                n_moves += 1
                break
        if not improved:
            break
    return movable, best_r, n_moves


CARVE_EDGE = 26.0  # A, auxiliary periodic cube the droplet is cut out of


def droplet_target_radius(n_bulk):
    """Radius holding `n_bulk` oxygens at bulk density, outside the ion's hole.

    The sphere of radius MIN_LN_O_BULK around the metal is occupied by the first
    coordination shell instead of bulk solvent, so it is excluded from the count.
    """
    v = n_bulk / RHO_WATER_NUM + 4.0 / 3.0 * np.pi * MIN_LN_O_BULK**3
    return (3.0 * v / (4.0 * np.pi)) ** (1 / 3)


def carve_droplet(n_bulk, rng, n_candidates=4000):
    """Bulk oxygen positions for a droplet, cut from a relaxed periodic liquid.

    Relaxing directly inside a hard sphere biases the result: the confining wall
    pushes surface molecules inwards with nothing pushing back, which leaves the
    outer shell 20-30% under-dense.  A periodic cube has no wall and therefore
    relaxes to a homogeneous liquid, so the droplet is carved out of one.

    Which point of that liquid becomes the metal site matters, because in a
    131-molecule sphere the local density fluctuates by several percent.  Rather
    than accept whichever fluctuation the centre happens to land in, many
    candidate centres are screened and the one whose surrounding oxygen count
    matches bulk density at the target radius is used.  Returns the positions
    centred on the origin.
    """
    n_carve = int(round(RHO_WATER_NUM * CARVE_EDGE**3))
    pts = rng.uniform(0.0, CARVE_EDGE, size=(n_carve, 3))
    pts, _, _ = relax_bulk_oxygens(
        np.zeros((0, 3)), pts, None, cell=CARVE_EDGE, rng=rng
    )

    r_target = droplet_target_radius(n_bulk)
    centres = rng.uniform(0.0, CARVE_EDGE, size=(n_candidates, 3))
    rel = pts[None, :, :] - centres[:, None, :]
    rel -= CARVE_EDGE * np.round(rel / CARVE_EDGE)
    r = np.linalg.norm(rel, axis=-1)
    count = ((r >= MIN_LN_O_BULK) & (r < r_target)).sum(axis=1)
    best = int(np.argmin(np.abs(count - n_bulk)))

    pts, r = rel[best], r[best]
    pts, r = pts[r >= MIN_LN_O_BULK], r[r >= MIN_LN_O_BULK]
    return pts[np.argsort(r)[:n_bulk]]


# --------------------------------------------------------------------------- #
# stage B: hydrogens
# --------------------------------------------------------------------------- #
def hbond_strength(d_ho, v_h_to_donor, v_h_to_acceptor):
    """Smooth 0..1 hydrogen-bond quality for an O-H...O arrangement.

    A Gaussian in the H...O acceptor distance times an angular term that
    switches on as the O-H...O geometry becomes linear.  All arguments are
    taken at the donated hydrogen.
    """
    n_don = np.maximum(np.linalg.norm(v_h_to_donor, axis=-1), 1e-6)
    cos = (v_h_to_donor * v_h_to_acceptor).sum(-1) / (d_ho * n_don)
    angular = (np.maximum(0.0, -cos - HB_COS_ONSET) / (1.0 - HB_COS_ONSET)) ** 2
    return np.exp(-(((d_ho - HB_R0) / HB_WIDTH) ** 2)) * angular


def orientation_scores(cand_pos, cand_is_h, ref_pos, ref_is_h, ref_don_vec, cell):
    """Score each trial orientation: steric overlap minus hydrogen bonding.

    `cand_pos` has shape (n_trial, n_atoms, 3) with the molecule's oxygen at
    index 0.  `ref_don_vec[i]` is the vector from reference atom i to the oxygen
    it is bonded to, and is zero for atoms that are not hydrogens.  The return
    value is (n_trial,) and lower is better.
    """
    d_vec = cand_pos[:, :, None, :] - ref_pos[None, None, :, :]
    if cell is not None:
        d_vec -= cell * np.round(d_vec / cell)
    dist = np.maximum(np.linalg.norm(d_vec, axis=-1), 1e-6)

    hh = cand_is_h[:, None] & ref_is_h[None, :]
    oo = (~cand_is_h)[:, None] & (~ref_is_h)[None, :]
    dmin = np.where(hh, PEN_HH, np.where(oo, PEN_OO, PEN_OH))
    score = W_STERIC * (np.maximum(0.0, dmin - dist) ** 2).sum(axis=(1, 2))

    # hydrogen bonds donated by the candidate to a reference oxygen
    ref_is_o = (~ref_is_h)[None, :]
    for k in np.flatnonzero(cand_is_h):
        strength = hbond_strength(
            dist[:, k, :],
            (cand_pos[:, 0, :] - cand_pos[:, k, :])[:, None, :],
            -d_vec[:, k, :, :],
        )
        score -= W_HBOND * (strength * ref_is_o).sum(-1)

    # hydrogen bonds accepted by the candidate's oxygen from a reference O-H
    donors = (ref_is_h & (np.linalg.norm(ref_don_vec, axis=-1) > 1e-6))[None, :]
    if donors.any():
        strength = hbond_strength(
            dist[:, 0, :], ref_don_vec[None, :, :], d_vec[:, 0, :, :]
        )
        score -= W_HBOND * (strength * donors).sum(-1)
    return score


@dataclass
class MolSpec:
    """A molecule whose oxygen is fixed and whose orientation is still free."""

    kind: str  # "oh" | "shell_water" | "bulk_water"
    o_pos: np.ndarray
    u_out: np.ndarray | None  # Ln->O axis for coordinated ligands

    @property
    def symbols(self):
        return ["O", "H"] if self.kind == "oh" else ["O", "H", "H"]

    def candidates(self, rng, n_trial):
        """(n_trial, n_atoms, 3) trial geometries for this molecule."""
        o = np.broadcast_to(self.o_pos, (n_trial, 1, 3))
        if self.kind == "oh":
            azim = np.linspace(0.0, 2 * np.pi, n_trial, endpoint=False)
            h = hydroxide_hydrogen(self.o_pos, self.u_out, azim)[:, None, :]
        elif self.kind == "shell_water":
            # the HOH plane is symmetric, so half a turn covers all orientations
            azim = np.linspace(0.0, np.pi, n_trial, endpoint=False)
            h = water_hydrogens(self.o_pos, self.u_out, azim)
        else:
            h = free_water_hydrogens(self.o_pos, random_rotations(rng, n_trial))
        return np.concatenate([o, h], axis=1)


def add_hydrogens(ln_pos, oh_o, shell_o, bulk_o, cell, rng, n_trial=N_TRIAL, n_sweep=N_SWEEP):
    """Orient every OH- and H2O, most constrained molecules first, then refine.

    Coordinated ligands have a single degree of freedom left (rotation about the
    Ln-O axis); bulk waters are free to adopt any orientation.  The first pass
    is sequential, so molecules placed early are blind to their later
    neighbours; the refinement sweeps re-optimise each molecule against the
    complete environment and keep the current geometry unless it is beaten.
    """
    specs = [MolSpec("oh", o, unit(o - ln_pos)) for o in oh_o]
    specs += [MolSpec("shell_water", o, unit(o - ln_pos)) for o in shell_o]
    specs += [MolSpec("bulk_water", o, None) for o in bulk_o]

    n_atoms = 1 + sum(len(s.symbols) for s in specs)
    pos = np.zeros((n_atoms, 3))
    don_vec = np.zeros((n_atoms, 3))  # H -> its own O, used for the acceptor term
    is_h = np.zeros(n_atoms, dtype=bool)
    pos[0] = ln_pos
    spans = []

    start = 1
    for spec in specs:  # reserve slots so refinement can address them
        spans.append((start, start + len(spec.symbols)))
        is_h[start : start + len(spec.symbols)] = [s == "H" for s in spec.symbols]
        start += len(spec.symbols)

    def store(lo, hi, geom):
        pos[lo:hi] = geom
        don_vec[lo + 1 : hi] = geom[0] - geom[1:]

    # --- pass 1: sequential placement against what already exists
    for spec, (lo, hi) in zip(specs, spans):
        cand = spec.candidates(rng, n_trial)
        scores = orientation_scores(
            cand, is_h[lo:hi], pos[:lo], is_h[:lo], don_vec[:lo], cell
        )
        store(lo, hi, cand[int(np.argmin(scores))])

    # --- passes 2..n: re-optimise each molecule against everything else
    for _ in range(n_sweep):
        gain = 0.0
        for spec, (lo, hi) in zip(specs, spans):
            keep = np.ones(n_atoms, dtype=bool)
            keep[lo:hi] = False
            cand = np.concatenate([pos[None, lo:hi], spec.candidates(rng, n_trial)])
            scores = orientation_scores(
                cand, is_h[lo:hi], pos[keep], is_h[keep], don_vec[keep], cell
            )
            best = int(np.argmin(scores))
            if best != 0:
                gain += scores[0] - scores[best]
                store(lo, hi, cand[best])
        if gain < 1e-6:
            break

    return [(s.symbols, pos[lo:hi].copy()) for s, (lo, hi) in zip(specs, spans)]


# --------------------------------------------------------------------------- #
# assembly
# --------------------------------------------------------------------------- #
@dataclass
class Sizing:
    n_water: int
    n_hydroxide: int
    box_length: float
    droplet_radius: float
    solvent_volume: float

    @staticmethod
    def compute(n_water=N_WATER, n_hydroxide=N_HYDROXIDE):
        """Size the cell/droplet from the *water* number density.

        The solvent (H2O plus OH-, which have essentially the same molar volume)
        sets the volume and Ln3+ is treated as volume-neutral.  That is the
        usual convention and is conservative here, since Ln3+ electrostriction
        makes its partial molar volume slightly negative.  Sizing on total
        *mass* instead would wrongly inflate the cell: an electrolyte solution
        has a mass density above 1 g/cm3 without the water being expanded.
        """
        v = (n_water + n_hydroxide) / RHO_WATER_NUM
        return Sizing(
            n_water=n_water,
            n_hydroxide=n_hydroxide,
            box_length=v ** (1 / 3),
            droplet_radius=(3.0 * v / (4.0 * np.pi)) ** (1 / 3),
            solvent_volume=v,
        )


def make_atoms(sym, ln_pos, molecules, multiplicity, geometry, boundary):
    symbols = [sym]
    positions = [ln_pos]
    for msyms, mpos in molecules:
        symbols += msyms
        positions.extend(mpos)

    atoms = Atoms(symbols=symbols, positions=np.array(positions))
    atoms.info.update(
        {
            # consumed by FAIRChemCalculator (omol task), mace_omol and mace_polar
            "charge": int(NET_CHARGE),
            "spin": int(multiplicity),
            "spin_multiplicity": int(multiplicity),
            "metal": sym,
            "geometry": geometry,
            "boundary": boundary,
        }
    )
    return atoms


def build_one(sym, sizing: Sizing, seed: int, verbose=True):
    """Return ({variant: Atoms}, build report) for one lanthanide."""
    info = LN_DATA[sym]
    mult = info["multiplicity"]
    n_shell_water = info["cn"] - N_HYDROXIDE
    n_bulk_water = sizing.n_water - n_shell_water
    out, report = {}, {}

    for geometry in ("box", "droplet"):
        rng = np.random.default_rng(seed + (0 if geometry == "box" else 10_000))

        if geometry == "box":
            cell = sizing.box_length
            radius = None
            ln_pos = np.full(3, cell / 2.0)  # Ln at the cube centre
            start = rng.uniform(0.0, cell, size=(n_bulk_water, 3))
        else:
            cell = None
            ln_pos = np.zeros(3)
            # No confining wall: inserting the first shell displaces solvent
            # outwards, and a wall would make the interior absorb that
            # displacement instead of letting the free surface relax.
            radius = None
            start = carve_droplet(n_bulk_water, rng)

        oh_o, shell_o, oh_sep = build_shell(sym, ln_pos, rng)
        shell_all = np.vstack([oh_o, shell_o])
        d_shell = np.linalg.norm(shell_all[:, None, :] - shell_all[None, :, :], axis=-1)
        shell_oo = float(d_shell[np.triu_indices(len(shell_all), 1)].min())

        bulk_o, n_it, worst = relax_bulk_oxygens(
            shell_all, start, ln_pos, cell=cell, radius=radius, rng=rng
        )
        bulk_o, cavity, n_moves = fill_voids(
            shell_all, bulk_o, ln_pos, cell=cell, radius=radius, rng=rng
        )
        if verbose:
            print(
                f"  {geometry:8s} relax {n_it:4d} iter (residual {worst:.1e} A), "
                f"{n_moves:3d} void moves -> largest cavity {cavity:.3f} A, "
                f"first-shell O-O >= {shell_oo:.3f} A"
            )
        report["min_shell_oo"] = shell_oo
        report[f"{geometry}_largest_cavity"] = cavity
        report[f"{geometry}_void_moves"] = n_moves

        molecules = add_hydrogens(ln_pos, oh_o, shell_o, bulk_o, cell, rng)

        if geometry == "box":
            atoms = make_atoms(sym, ln_pos, molecules, mult, "box", "pbc")
            atoms.set_cell([cell] * 3)
            atoms.set_pbc(True)
            out["box_pbc"] = atoms

            free = atoms.copy()  # byte-identical coordinates, periodicity removed
            free.info = dict(atoms.info, boundary="non-pbc")
            free.set_cell(np.zeros((3, 3)))
            free.set_pbc(False)
            out["box_nonpbc"] = free
        else:
            atoms = make_atoms(sym, ln_pos, molecules, mult, "droplet", "non-pbc")
            o_r = np.linalg.norm(
                atoms.positions[np.array(atoms.get_chemical_symbols()) == "O"] - ln_pos,
                axis=1,
            )
            atoms.info["droplet_radius"] = round(float(o_r.max()), 4)
            report["droplet_radius"] = atoms.info["droplet_radius"]
            out["droplet_nonpbc"] = atoms

            padded = atoms.copy()
            padded.info = dict(atoms.info, boundary="pbc")
            box = float(np.ptp(padded.positions, axis=0).max() + VACUUM_GAP)
            padded.set_cell([box] * 3)
            padded.set_pbc(True)
            padded.center()
            out["droplet_pbc"] = padded
            report["droplet_cell"] = box

        report[f"{geometry}_relax_iterations"] = n_it
        report[f"{geometry}_residual_overlap"] = worst

    report.update(
        coordination_number=info["cn"],
        n_shell_water=n_shell_water,
        n_bulk_water=n_bulk_water,
        min_oh_oh_shell=oh_sep,
        multiplicity=mult,
        n_unpaired=info["n_unpaired"],
        d_ln_oh=info["d_oh"],
        d_ln_ow=info["d_ow"],
    )
    return out, report


VARIANTS = ("box_pbc", "box_nonpbc", "droplet_pbc", "droplet_nonpbc")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="structures", help="output directory")
    ap.add_argument("--seed", type=int, default=20260901)
    ap.add_argument("--metals", nargs="*", default=list(LN_DATA))
    args = ap.parse_args()

    sizing = Sizing.compute()
    root = Path(args.out)
    for v in VARIANTS:
        (root / v).mkdir(parents=True, exist_ok=True)

    print(
        f"solvent: {sizing.n_water} H2O + {sizing.n_hydroxide} OH-\n"
        f"  V              = {sizing.solvent_volume:.1f} A^3 "
        f"({RHO_WATER_MASS} g/cm3, {RHO_WATER_NUM} molecules/A^3)\n"
        f"  cube edge      = {sizing.box_length:.3f} A\n"
        f"  droplet radius = {sizing.droplet_radius:.3f} A (oxygen centres)\n"
    )

    manifest = {
        "composition": {
            "n_water": N_WATER,
            "n_hydroxide": N_HYDROXIDE,
            "n_atoms": 1 + 2 * N_HYDROXIDE + 3 * N_WATER,
            "net_charge": NET_CHARGE,
        },
        "sizing": asdict(sizing),
        "vacuum_gap": VACUUM_GAP,
        "build": {},
        "systems": {},
    }

    all_frames = []
    for i, sym in enumerate(args.metals):
        print(f"[{sym}]  CN={LN_DATA[sym]['cn']}  2S+1={LN_DATA[sym]['multiplicity']}")
        systems, report = build_one(sym, sizing, args.seed + 977 * i)
        for variant, atoms in systems.items():
            name = f"{sym}-3OH-{N_WATER}H2O_{variant}"
            path = root / variant / f"{name}.xyz"
            write(path, atoms, format="extxyz")
            all_frames.append(atoms)
            manifest["systems"][name] = {
                "file": str(path.relative_to(root)),
                "metal": sym,
                "variant": variant,
                "n_atoms": len(atoms),
                "charge": atoms.info["charge"],
                "spin_multiplicity": atoms.info["spin"],
                "pbc": bool(atoms.pbc.all()),
                "cell": atoms.cell.lengths().tolist() if atoms.pbc.any() else None,
            }
        manifest["build"][sym] = report
        print()

    write(root / "all_systems.extxyz", all_frames, format="extxyz")
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"wrote {len(all_frames)} structures under {root}/")


if __name__ == "__main__":
    main()
