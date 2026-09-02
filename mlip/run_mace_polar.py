#!/usr/bin/env python3
"""Single-point evaluation with MACE-POLAR-1 (polarisable electrostatic MACE).

MACE-POLAR-1 enforces the total charge and spin through learnable Fukui
equilibration functions, and additionally accepts an external electric field:

    atoms.info["charge"]         = 0
    atoms.info["spin"]           = 8            # spin multiplicity 2S+1
    atoms.info["external_field"] = [0.0, 0.0, 0.0]

Because it predicts spin-resolved atomic multipoles, it also returns per-atom
charges and the total dipole, which are reported here: for a hydrated Ln(3+)
they are a useful check on whether the ion is described as trivalent and how
much charge the three hydroxides retain.

Install (MACE >= 0.3.16, plus the long-range extension):

    pip install --upgrade mace-torch
    pip install git+https://github.com/WillBaldwin0/graph_electrostatics

Variants: polar-1-m (2 layers, 12 A receptive field), polar-1-l (3 layers, 18 A).
The droplet cells carry 22 A of vacuum, which clears even polar-1-l.

Examples:

    python run_mace_polar.py --dry-run
    python run_mace_polar.py "droplet_nonpbc/*.xyz" --model polar-1-m
    python run_mace_polar.py --variants droplet_nonpbc --field 0 0 0.01
"""

from __future__ import annotations

import numpy as np

import common


def make_calc(args):
    from mace.calculators import mace_polar

    return mace_polar(
        model=args.model, device=args.device, default_dtype=args.dtype
    )


def main():
    ap = common.parser(__doc__)
    ap.add_argument("--model", default="polar-1-m", choices=["polar-1-m", "polar-1-l"])
    ap.add_argument(
        "--field",
        nargs=3,
        type=float,
        default=[0.0, 0.0, 0.0],
        metavar=("EX", "EY", "EZ"),
        help="external electric field in V/A",
    )
    args = ap.parse_args()

    def extra_setup(atoms):
        atoms.info["external_field"] = list(args.field)

    def extra_results(calc, atoms):
        out = {"external_field_V_per_A": list(args.field)}
        charges = calc.results.get("charges")
        if charges is None:
            return out
        charges = np.asarray(charges)
        symbols = np.array(atoms.get_chemical_symbols())
        metal = atoms.info["metal"]
        out["metal_charge_e"] = float(charges[symbols == metal][0])
        out["total_charge_e"] = float(charges.sum())
        out["mean_O_charge_e"] = float(charges[symbols == "O"].mean())
        out["mean_H_charge_e"] = float(charges[symbols == "H"].mean())
        dipole = calc.results.get("dipole")
        if dipole is not None:
            out["dipole_eA"] = np.asarray(dipole).tolist()
        return out

    common.run(
        f"mace-{args.model}",
        make_calc,
        args,
        extra_setup=extra_setup,
        extra_results=extra_results,
    )


if __name__ == "__main__":
    main()
