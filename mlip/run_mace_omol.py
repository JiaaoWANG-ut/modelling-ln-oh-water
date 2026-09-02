#!/usr/bin/env python3
"""Single-point evaluation with MACE-OMOL.

MACE-OMOL embeds the total charge and total spin as global scalars that are
added to the initial node features, so both must be supplied:

    atoms.info["charge"] = 0
    atoms.info["spin"]   = 8      # spin multiplicity 2S+1

Install (MACE >= 0.3.14):

    pip install --upgrade mace-torch

Examples:

    python run_mace_omol.py --dry-run
    python run_mace_omol.py "droplet_nonpbc/*.xyz" --model extra_large
    python run_mace_omol.py --variants box_pbc --dtype float32
"""

from __future__ import annotations

import common


def make_calc(args):
    from mace.calculators import mace_omol

    return mace_omol(
        model=args.model, device=args.device, default_dtype=args.dtype
    )


def main():
    ap = common.parser(__doc__)
    ap.add_argument(
        "--model",
        default="extra_large",
        help="extra_large (default) or a smaller head; the small variant is "
        "more robust for strongly charged clusters",
    )
    args = ap.parse_args()
    common.run(f"mace-omol-{args.model}", make_calc, args)


if __name__ == "__main__":
    main()
