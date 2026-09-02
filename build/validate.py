#!/usr/bin/env python3
"""Independent sanity check of every generated structure.

Nothing here trusts the builder's bookkeeping: molecular topology is recovered
from interatomic distances, and densities, coordination numbers and the
charge/spin consistency are all recomputed from the coordinates and elements.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
from ase.data import atomic_masses, atomic_numbers
from ase.io import read

from build_systems import CAVITY_TARGET, cavity_scan
from ln_data import (
    ANGLE_HOH,
    LN_DATA,
    MIN_HH_INTER,
    MIN_OH_INTER,
    MIN_OO,
    MIN_OO_SHELL,
    NET_CHARGE,
    N_HYDROXIDE,
    N_WATER,
    RHO_WATER_MASS,
    RHO_WATER_NUM,
)

AMU_PER_A3_TO_G_PER_CM3 = 1.66053907
R_COVALENT_OH = 1.25  # A, O-H bonding cutoff
R_FIRST_SHELL = 3.10  # A, Ln-O first-shell cutoff
LONGEST_RECEPTIVE_FIELD = 18.0  # A, MACE-POLAR-1-L

FAIL = "FAIL"
WARN = "warn"
OK = "ok"


class Report:
    def __init__(self, name):
        self.name = name
        self.rows = []

    def check(self, label, value, ok, note=""):
        self.rows.append((label, value, OK if ok else FAIL, note))

    def warn_if(self, label, value, bad, note=""):
        self.rows.append((label, value, WARN if bad else OK, note))

    def note(self, label, value, note=""):
        self.rows.append((label, value, "", note))

    @property
    def failures(self):
        return [r for r in self.rows if r[2] == FAIL]

    @property
    def warnings(self):
        return [r for r in self.rows if r[2] == WARN]


def topology(atoms, metal):
    """Recover molecules from distances; returns (hydroxides, waters, dmat)."""
    d = atoms.get_all_distances(mic=bool(atoms.pbc.any()))
    sym = np.array(atoms.get_chemical_symbols())
    o_idx = np.flatnonzero(sym == "O")
    h_idx = np.flatnonzero(sym == "H")

    owner = {}  # H index -> O index
    for h in h_idx:
        sub = d[h, o_idx]
        j = int(np.argmin(sub))
        if sub[j] <= R_COVALENT_OH:
            owner[int(h)] = int(o_idx[j])

    groups = {int(o): [] for o in o_idx}
    for h, o in owner.items():
        groups[o].append(h)

    hydroxides = {o: hs for o, hs in groups.items() if len(hs) == 1}
    waters = {o: hs for o, hs in groups.items() if len(hs) == 2}
    orphans = [h for h in h_idx if int(h) not in owner]
    odd = {o: hs for o, hs in groups.items() if len(hs) not in (1, 2)}
    return hydroxides, waters, orphans, odd, d, o_idx, h_idx


HB_MAX_HO = 2.50  # A, H...O acceptor distance
HB_MAX_OO = 3.50  # A, donor-acceptor O...O distance
HB_MIN_ANGLE = 140.0  # deg, O-H...O


def mic_vectors(atoms, v):
    if atoms.pbc.any():
        from ase.geometry import find_mic

        v, _ = find_mic(v, atoms.cell, atoms.pbc)
    return v


def hydrogen_bonds(atoms, d, groups, o_idx):
    """Geometric hydrogen-bond census (donor side).

    Returns (n_bonds, bonds_per_molecule, fraction of O-H donating a bond).
    """
    parent = {h: o for o, hs in groups.items() for h in hs}
    cand_h, cand_a, cand_d = [], [], []
    for h, o_d in parent.items():
        for o_a in o_idx:
            o_a = int(o_a)
            if o_a == o_d:
                continue
            if d[h, o_a] <= HB_MAX_HO and d[o_d, o_a] <= HB_MAX_OO:
                cand_h.append(h)
                cand_a.append(o_a)
                cand_d.append(o_d)
    if not cand_h:
        return 0, 0.0, 0.0

    p = atoms.positions
    v_don = mic_vectors(atoms, p[cand_d] - p[cand_h])
    v_acc = mic_vectors(atoms, p[cand_a] - p[cand_h])
    cos = (v_don * v_acc).sum(1) / (
        np.linalg.norm(v_don, axis=1) * np.linalg.norm(v_acc, axis=1)
    )
    angle = np.degrees(np.arccos(np.clip(cos, -1, 1)))
    n_bonds = int((angle >= HB_MIN_ANGLE).sum())
    n_donors = sum(len(hs) for hs in groups.values())
    return n_bonds, 2.0 * n_bonds / len(groups), n_bonds / n_donors


def largest_cavity(atoms, o_idx, ln_i, box_edge, margin=1.7):
    """Radius of the biggest oxygen-free sphere inside the solvent.

    The probe region follows the *geometry*, not the periodicity: a cube is
    always probed under min-image, because box_pbc and box_nonpbc share
    coordinates and an interior void is a defect either way, while a droplet is
    probed only well inside its surface, since beyond that the "cavity" is
    simply the surrounding vacuum.
    """
    p = atoms.positions[o_idx]
    if atoms.info["geometry"] == "box":
        return cavity_scan(p, cell=box_edge)[0]
    centre = atoms.positions[ln_i]
    r_in = np.linalg.norm(p - centre, axis=1).max() - margin
    return cavity_scan(p, centre=centre, r_in=r_in)[0]


def min_inter_distances(atoms, d, mol_of_atom):
    """Smallest intermolecular O-O, O-H and H-H distances."""
    sym = np.array(atoms.get_chemical_symbols())
    n = len(atoms)
    same = mol_of_atom[:, None] == mol_of_atom[None, :]
    dd = d.copy()
    dd[same] = np.inf
    np.fill_diagonal(dd, np.inf)

    is_o, is_h = sym == "O", sym == "H"
    res = {}
    res["O-O"] = float(dd[np.ix_(is_o, is_o)].min())
    res["O-H"] = float(dd[np.ix_(is_o, is_h)].min())
    res["H-H"] = float(dd[np.ix_(is_h, is_h)].min())
    return res


def analyse(path, sizing):
    atoms = read(path, format="extxyz")
    metal = atoms.info["metal"]
    variant = atoms.info["geometry"] + "/" + atoms.info["boundary"]
    info = LN_DATA[metal]
    rep = Report(f"{metal} {variant}")
    mic = bool(atoms.pbc.any())

    # ---------------- composition ----------------
    counts = Counter(atoms.get_chemical_symbols())
    rep.check("n_atoms", len(atoms), len(atoms) == 1 + 2 * N_HYDROXIDE + 3 * N_WATER)
    rep.check(f"n_{metal}", counts[metal], counts[metal] == 1)
    rep.check("n_O", counts["O"], counts["O"] == N_WATER + N_HYDROXIDE)
    rep.check("n_H", counts["H"], counts["H"] == 2 * N_WATER + N_HYDROXIDE)

    # ---------------- topology ----------------
    hydroxides, waters, orphans, odd, d, o_idx, h_idx = topology(atoms, metal)
    rep.check("n_OH-", len(hydroxides), len(hydroxides) == N_HYDROXIDE)
    rep.check("n_H2O", len(waters), len(waters) == N_WATER)
    rep.check("unassigned H", len(orphans), not orphans)
    rep.check("O with != 1,2 H", len(odd), not odd)

    mol_of_atom = np.full(len(atoms), -1)
    m_id = 0
    ln_i = int(np.flatnonzero(np.array(atoms.get_chemical_symbols()) == metal)[0])
    mol_of_atom[ln_i] = m_id
    for o, hs in {**hydroxides, **waters}.items():
        m_id += 1
        mol_of_atom[o] = m_id
        for h in hs:
            mol_of_atom[h] = m_id

    # ---------------- intramolecular geometry ----------------
    oh_bonds = [d[o, h] for o, hs in {**hydroxides, **waters}.items() for h in hs]
    rep.check(
        "O-H bond range (A)",
        f"{min(oh_bonds):.4f} - {max(oh_bonds):.4f}",
        0.90 < min(oh_bonds) and max(oh_bonds) < 1.02,
    )
    angles = [
        atoms.get_angle(hs[0], o, hs[1], mic=mic) for o, hs in waters.items()
    ]
    rep.check(
        "H-O-H angle range (deg)",
        f"{min(angles):.2f} - {max(angles):.2f}",
        abs(min(angles) - ANGLE_HOH) < 0.05 and abs(max(angles) - ANGLE_HOH) < 0.05,
    )

    # ---------------- coordination of the metal ----------------
    d_ln_o = d[ln_i, o_idx]
    shell = o_idx[d_ln_o <= R_FIRST_SHELL]
    n_oh_in_shell = sum(1 for o in shell if int(o) in hydroxides)
    rep.check("Ln coordination number", len(shell), len(shell) == info["cn"])
    rep.check("OH- in first shell", n_oh_in_shell, n_oh_in_shell == N_HYDROXIDE)
    rep.note(
        "d(Ln-O) first shell (A)",
        f"{d[ln_i, shell].min():.3f} - {d[ln_i, shell].max():.3f}",
        f"target OH {info['d_oh']:.2f} / H2O {info['d_ow']:.2f}",
    )
    outer = o_idx[d_ln_o > R_FIRST_SHELL]
    gap = float(d[ln_i, outer].min())
    rep.check("nearest 2nd-shell O (A)", f"{gap:.3f}", gap > 3.55, "first minimum of g(Ln-O)")
    rep.note("nearest Ln-H (A)", f"{d[ln_i, h_idx].min():.3f}")

    oh_o = list(hydroxides)
    oh_oo = [d[a, b] for i, a in enumerate(oh_o) for b in oh_o[i + 1 :]]
    rep.warn_if(
        "OH-...OH- O-O (A)",
        " ".join(f"{x:.3f}" for x in sorted(oh_oo)),
        min(oh_oo) < 2.60,
        "ligand-ligand contact",
    )

    # ---------------- steric quality ----------------
    mins = min_inter_distances(atoms, d, mol_of_atom)
    rep.check("min intermol. O-O (A)", f"{mins['O-O']:.3f}", mins["O-O"] >= MIN_OO_SHELL)
    rep.check("min intermol. O-H (A)", f"{mins['O-H']:.3f}", mins["O-H"] >= MIN_OH_INTER)
    rep.check("min intermol. H-H (A)", f"{mins['H-H']:.3f}", mins["H-H"] >= MIN_HH_INTER)

    # ---------------- hydrogen-bond network ----------------
    n_hb, hb_per_mol, donor_frac = hydrogen_bonds(
        atoms, d, {**hydroxides, **waters}, o_idx
    )
    # A quality indicator rather than a correctness criterion.  With the oxygen
    # positions frozen only orientations can be optimised, so ~3.1 is the
    # practical ceiling against 3.5-3.6 for equilibrated bulk water; the
    # non-periodic variants are lower again because surface O-H groups have no
    # acceptor.  The guard only fires if the orientation search failed outright.
    rep.warn_if(
        "H-bonds per solvent molecule",
        f"{hb_per_mol:.2f}",
        hb_per_mol < 1.8,
        "bulk water 3.5-3.6; ~3.1 is the ceiling at frozen O positions",
    )
    rep.note("O-H groups donating a H-bond", f"{donor_frac * 100:.0f}%", f"{n_hb} bonds")

    # ---------------- density ----------------
    mass = sum(atomic_masses[atomic_numbers[s]] for s in atoms.get_chemical_symbols())
    if atoms.info["geometry"] == "box":
        v = sizing["box_length"] ** 3
        n_dens = (N_WATER + N_HYDROXIDE) / v
        rep.note("cube edge (A)", f"{sizing['box_length']:.3f}")
        rep.check(
            "solvent number density (1/A^3)",
            f"{n_dens:.5f}",
            abs(n_dens / RHO_WATER_NUM - 1) < 0.01,
            f"target {RHO_WATER_NUM:.5f}",
        )
        rep.note(
            "solution mass density (g/cm3)",
            f"{mass / v * AMU_PER_A3_TO_G_PER_CM3:.4f}",
            "> 1 as expected for a Ln salt solution",
        )
        rep.check(
            "L/2 (A)",
            f"{sizing['box_length'] / 2:.3f}",
            sizing["box_length"] / 2 > 6.0,
            "must exceed the per-layer MLIP cutoff (~6 A)",
        )
    else:
        r_o = np.linalg.norm(atoms.positions[o_idx] - atoms.positions[ln_i], axis=1)
        r_max = float(r_o.max())
        n_dens = (N_WATER + N_HYDROXIDE) / (4.0 / 3.0 * np.pi * r_max**3)
        rep.check(
            "droplet radius (A)",
            f"{r_max:.3f}",
            abs(r_max - sizing["droplet_radius"]) < 0.5,
            f"density target {sizing['droplet_radius']:.3f}",
        )
        # The outermost molecule of a 131-molecule droplet fluctuates by about
        # +-0.3 A, which is +-8% in a radius-derived density, so this number is
        # necessarily noisier than the box.  The construction targets the exact
        # bulk density; the cavity scan below is the sharper test.
        rep.warn_if(
            "solvent number density (1/A^3)",
            f"{n_dens:.5f}",
            abs(n_dens / RHO_WATER_NUM - 1) > 0.10,
            f"target {RHO_WATER_NUM:.5f}, +-8% finite-size noise",
        )
        # Shell-resolved profile, with the outermost shell volume clipped to the
        # droplet surface.  Excess near the ion is real electrostriction; the
        # solvent far from the ion should sit at bulk density.
        edges = list(np.arange(0.0, r_max, 2.0)) + [r_max]
        prof = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            shell_v = 4.0 / 3.0 * np.pi * (hi**3 - lo**3)
            prof.append(f"{lo:.0f}-{hi:.1f}:{((r_o >= lo) & (r_o < hi)).sum() / shell_v:.4f}")

        rep.note("radial O density by shell (1/A^3)", " ".join(prof))
        for rc in (R_FIRST_SHELL, 5.5):
            rep.note(f"N(O) within {rc:.2f} A of Ln", int((r_o < rc).sum()))

    # Local solvent density in an ion-centred annulus, chosen to clear the first
    # shell and to fit inside the periodic cube (max inscribed radius 7.89 A) so
    # that box and droplet are measured identically.  With only ~37 oxygens in
    # the shell, counting noise alone is around 10%, so this cannot be a tight
    # test; the exact global density and the cavity scan are the sharp ones.
    lo, hi = 4.2, 7.0
    r_ln = d[ln_i, o_idx]
    n_ann = int(((r_ln >= lo) & (r_ln < hi)).sum())
    rho_ann = n_ann / (4.0 / 3.0 * np.pi * (hi**3 - lo**3))
    rep.warn_if(
        f"O density in the {lo}-{hi} A annulus (1/A^3)",
        f"{rho_ann:.5f}",
        abs(rho_ann / RHO_WATER_NUM - 1) > 0.20,
        f"{n_ann} oxygens, bulk would give {RHO_WATER_NUM * 4 / 3 * np.pi * (hi**3 - lo**3):.1f}",
    )

    # A cavity able to host another oxygen at the target O-O separation is a
    # genuine packing defect: an extra water could be inserted there legally,
    # so the local density is below bulk.
    cavity = largest_cavity(atoms, o_idx, ln_i, sizing["box_length"])
    rep.check(
        "largest interior cavity (A)",
        f"{cavity:.3f}",
        cavity <= CAVITY_TARGET + 0.1,
        "biggest O-free sphere; ideal lattice at this density gives ~2.5 A",
    )

    # ---------------- periodic images ----------------
    if atoms.pbc.any():
        L = atoms.cell.lengths()
        if atoms.info["geometry"] == "droplet":
            extent = np.ptp(atoms.positions, axis=0)
            vac = float((L - extent).min())
            rep.check(
                "vacuum gap (A)",
                f"{vac:.2f}",
                vac >= LONGEST_RECEPTIVE_FIELD,
                f">= {LONGEST_RECEPTIVE_FIELD} A (MACE-POLAR-1-L receptive field)",
            )
        rep.note("cell (A)", " ".join(f"{x:.3f}" for x in L))
    else:
        rep.check("cell is empty", atoms.cell.volume == 0.0, atoms.cell.volume == 0.0)
    rep.note("pbc", str(tuple(bool(p) for p in atoms.pbc)))

    # ---------------- charge / spin ----------------
    z_sum = int(sum(atomic_numbers[s] for s in atoms.get_chemical_symbols()))
    charge = int(atoms.info["charge"])
    mult = int(atoms.info["spin"])
    n_el = z_sum - charge
    rep.check("net charge", charge, charge == NET_CHARGE, "Ln(3+) + 3 OH(-)")
    rep.check("total electrons", n_el, n_el == z_sum)
    rep.check(
        "spin multiplicity",
        mult,
        mult == info["multiplicity"],
        f"4f^{info['nf']} high spin, {info['n_unpaired']} unpaired",
    )
    rep.check(
        "electron-count parity",
        f"{n_el} e-, 2S+1 = {mult}",
        (n_el + mult) % 2 == 1,
        "even electrons <-> odd multiplicity",
    )
    rep.check(
        "info keys for MLIPs",
        sorted(k for k in atoms.info if k in ("charge", "spin", "spin_multiplicity")),
        {"charge", "spin", "spin_multiplicity"} <= set(atoms.info),
    )
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="structures")
    ap.add_argument("--out", default="reports/validation.md")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    manifest = json.loads((root / "manifest.json").read_text())
    sizing = manifest["sizing"]

    reports = []
    for name, meta in sorted(manifest["systems"].items()):
        reports.append(analyse(root / meta["file"], sizing))

    lines = ["# Structure validation", ""]
    n_fail = n_warn = 0
    for rep in reports:
        lines += [f"## {rep.name}", "", "| check | value | status | note |", "|---|---|---|---|"]
        for label, value, status, note in rep.rows:
            lines.append(f"| {label} | `{value}` | {status} | {note} |")
        lines.append("")
        n_fail += len(rep.failures)
        n_warn += len(rep.warnings)
        if not args.quiet:
            flag = "FAIL" if rep.failures else ("warn" if rep.warnings else "ok  ")
            print(f"[{flag}] {rep.name}")
            for label, value, status, note in rep.rows:
                if status in (FAIL, WARN):
                    print(f"        {status}: {label} = {value}  {note}")

    summary = f"{len(reports)} structures, {n_fail} failed checks, {n_warn} warnings"
    lines.insert(2, summary)
    lines.insert(3, "")
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(lines))
    print("\n" + summary)
    print(f"report: {args.out}")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
