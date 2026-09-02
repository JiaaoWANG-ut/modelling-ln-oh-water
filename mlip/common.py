"""Shared plumbing for the UMA / MACE-OMOL / MACE-POLAR-1 drivers.

All three models read the total charge and the *spin multiplicity* (2S+1) from
`atoms.info`, using the same key names:

    atoms.info["charge"] = 0     # net charge, in units of e
    atoms.info["spin"]   = 8     # 2S+1, i.e. unpaired electrons + 1

so the only thing that differs between them is how the calculator is built.
This module re-derives charge and spin from the elements rather than trusting
whatever is written in the structure file, and refuses to run if they disagree.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
from ase.data import atomic_numbers
from ase.io import read

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))

from ln_data import LN_DATA, NET_CHARGE, N_HYDROXIDE, N_WATER  # noqa: E402

# OMol25 covers elements 1-83, so every lanthanide here is in the training set,
# but the paper flags lanthanide complexes as sparsely represented and states
# that only high-spin states were generated for them.  The multiplicities below
# are therefore both the physically correct free-ion ground states and the only
# spin states these models ever saw for these elements.
OMOL25_NOTE = (
    "OMol25 covers Z = 1-83 including all lanthanides, but lanthanide complexes "
    "are sparsely represented and only high-spin states were computed. Treat "
    "these predictions as extrapolation and validate against DFT."
)


def expected_charge_spin(atoms):
    """Net charge and multiplicity implied by the composition.

    The hydroxides and waters are closed shell, so the whole system's spin is
    that of the free Ln(3+) ion in its Hund's-rule ground state.
    """
    symbols = atoms.get_chemical_symbols()
    metals = sorted({s for s in symbols if s in LN_DATA})
    if len(metals) != 1:
        raise ValueError(f"expected exactly one lanthanide, found {metals}")
    metal = metals[0]
    return metal, NET_CHARGE, LN_DATA[metal]["multiplicity"]


def load_system(path, *, strict=True):
    """Read a structure and stamp on the charge / spin keys the models need."""
    atoms = read(path, format="extxyz")
    metal, charge, mult = expected_charge_spin(atoms)

    for key, want in (("charge", charge), ("spin", mult)):
        got = atoms.info.get(key)
        if got is not None and int(got) != want:
            msg = f"{Path(path).name}: info['{key}'] is {got} but composition implies {want}"
            if strict:
                raise ValueError(msg)
            print(f"  warning: {msg}", file=sys.stderr)

    atoms.info["charge"] = charge
    atoms.info["spin"] = mult  # 2S+1, the key UMA and MACE both read
    atoms.info["spin_multiplicity"] = mult  # some wrappers look for this name
    atoms.info["metal"] = metal
    return atoms


def collect_paths(root, patterns, variants=None):
    """Resolve CLI selectors into a sorted list of structure files."""
    root = Path(root)
    paths = []
    for pat in patterns:
        p = Path(pat)
        if p.is_file():
            paths.append(p)
        else:
            paths.extend(sorted(root.glob(pat)))
    if variants:
        paths = [p for p in paths if p.parent.name in variants]
    seen, unique = set(), []
    for p in paths:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def add_common_args(ap):
    ap.add_argument(
        "structures",
        nargs="*",
        default=["*/*.xyz"],
        help="files or glob patterns relative to --root",
    )
    ap.add_argument("--root", default=str(ROOT / "structures"))
    ap.add_argument(
        "--variants",
        nargs="*",
        choices=["box_pbc", "box_nonpbc", "droplet_pbc", "droplet_nonpbc"],
        help="restrict to these boundary-condition variants",
    )
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    ap.add_argument("--dtype", default="float64", choices=["float32", "float64"])
    ap.add_argument("--out", default=None, help="JSON results file")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="check structures, charge and spin without loading a model",
    )
    return ap


def warn_if_periodic(atoms, engine):
    """Flag the out-of-domain case: a periodic cell with a molecular model.

    All three models are trained on OMol25, which is a molecular (non-periodic)
    dataset.  They can still be evaluated under periodic boundary conditions,
    and MACE-POLAR-1 handles the long-range term in a cell, but bulk liquid
    under PBC is outside the training distribution.  The droplet_pbc variant is
    safe by construction: it is a cluster in >= 22 A of vacuum, which exceeds
    every model's receptive field, so it must reproduce droplet_nonpbc.
    """
    if not atoms.pbc.any():
        return None
    if atoms.info.get("geometry") == "droplet":
        return "droplet in vacuum: should match the non-pbc result to ~0"
    return f"{engine} is OMol25-trained (molecular); dense PBC liquid is out of domain"


def single_point(atoms, calc, *, want_stress=None):
    """Energy, forces and timing for one structure."""
    atoms.calc = calc
    if want_stress is None:
        want_stress = bool(atoms.pbc.all())

    t0 = time.perf_counter()
    energy = float(atoms.get_potential_energy())
    forces = np.asarray(atoms.get_forces())
    stress = None
    if want_stress:
        try:
            stress = np.asarray(atoms.get_stress(voigt=True)).tolist()
        except Exception as exc:  # not every model exposes a stress
            stress = f"unavailable: {type(exc).__name__}: {exc}"
    wall = time.perf_counter() - t0

    fnorm = np.linalg.norm(forces, axis=1)
    return {
        "energy_eV": energy,
        "energy_per_atom_eV": energy / len(atoms),
        "max_force_eV_per_A": float(fnorm.max()),
        "rms_force_eV_per_A": float(np.sqrt((fnorm**2).mean())),
        "force_on_metal_eV_per_A": float(
            fnorm[atoms.get_chemical_symbols().index(atoms.info["metal"])]
        ),
        "net_force_eV_per_A": np.abs(forces.sum(axis=0)).max().item(),
        "stress_eV_per_A3": stress,
        "wall_seconds": wall,
    }


def run(engine, make_calc, args, extra_setup=None, extra_results=None):
    """Drive `engine` over the selected structures and write a JSON report.

    `make_calc` is called once, lazily, so that --dry-run needs no model.
    `extra_setup(atoms)` may add engine-specific info keys, and
    `extra_results(calc, atoms)` may pull engine-specific outputs.
    """
    paths = collect_paths(args.root, args.structures, args.variants)
    if not paths:
        raise SystemExit(f"no structures matched under {args.root}")

    print(f"engine: {engine}")
    print(f"note:   {OMOL25_NOTE}\n")

    calc = None
    results = {}
    for path in paths:
        atoms = load_system(path)
        metal = atoms.info["metal"]
        tag = f"{path.parent.name}/{path.stem}"
        head = (
            f"{tag}\n"
            f"    {len(atoms):3d} atoms  {metal}(3+) + {N_HYDROXIDE} OH- + {N_WATER} H2O"
            f"  charge {atoms.info['charge']}  2S+1 = {atoms.info['spin']}"
            f"  ({LN_DATA[metal]['n_unpaired']} unpaired, 4f^{LN_DATA[metal]['nf']})"
        )
        print(head)
        caveat = warn_if_periodic(atoms, engine)
        if caveat:
            print(f"    caveat: {caveat}")

        entry = {
            "file": str(path),
            "metal": metal,
            "variant": path.parent.name,
            "n_atoms": len(atoms),
            "charge": atoms.info["charge"],
            "spin_multiplicity": atoms.info["spin"],
            "n_unpaired": LN_DATA[metal]["n_unpaired"],
            "pbc": bool(atoms.pbc.all()),
            "caveat": caveat,
        }

        if args.dry_run:
            results[tag] = entry
            print("    dry run: charge and spin verified, model not loaded\n")
            continue

        if calc is None:
            print("    loading model ...")
            calc = make_calc(args)
        if extra_setup:
            extra_setup(atoms)

        entry.update(single_point(atoms, calc))
        if extra_results:
            entry.update(extra_results(calc, atoms))
        print(
            f"    E = {entry['energy_eV']:.6f} eV"
            f"  ({entry['energy_per_atom_eV']:.6f} eV/atom)\n"
            f"    |F|max = {entry['max_force_eV_per_A']:.4f}"
            f"  |F|rms = {entry['rms_force_eV_per_A']:.4f}"
            f"  |F| on {metal} = {entry['force_on_metal_eV_per_A']:.4f} eV/A"
            f"  [{entry['wall_seconds']:.2f} s]\n"
        )
        results[tag] = entry

    out = Path(args.out) if args.out else ROOT / "reports" / f"{engine}_singlepoint.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "engine": engine,
                "args": {k: v for k, v in vars(args).items()},
                "python": platform.python_version(),
                "note": OMOL25_NOTE,
                "results": results,
            },
            indent=2,
        )
    )
    print(f"wrote {out}")


def parser(description):
    return add_common_args(
        argparse.ArgumentParser(
            description=description, formatter_class=argparse.RawDescriptionHelpFormatter
        )
    )
