#!/usr/bin/env python3
"""Single-point evaluation with UMA (fairchem v2), omol task.

The omol task is the only UMA task that accepts a charge and a spin state, so it
is the one to use for these systems.  Both are read from `atoms.info`:

    atoms.info["charge"] = 0
    atoms.info["spin"]   = 8      # spin multiplicity 2S+1

Install (needs a Hugging Face token; the UMA weights are gated):

    pip install fairchem-core
    hf auth login

Examples:

    python run_uma.py --dry-run
    python run_uma.py "droplet_nonpbc/*.xyz" --model uma-s-1p2
    python run_uma.py --variants droplet_pbc droplet_nonpbc --dtype float32
"""

from __future__ import annotations

import common


def make_calc(args):
    from fairchem.core import FAIRChemCalculator, pretrained_mlip

    predictor = pretrained_mlip.get_predict_unit(args.model, device=args.device)
    return FAIRChemCalculator(predictor, task_name=args.task)


def main():
    ap = common.parser(__doc__)
    ap.add_argument(
        "--model",
        default="uma-s-1p2",
        help="uma-s-1p2 (UMA 1.2 small, default), uma-s-1p1, uma-m-1p1",
    )
    ap.add_argument(
        "--task",
        default="omol",
        choices=["omol", "omat", "omc", "oc20", "oc22", "oc25", "odac"],
        help="omol is the only task that consumes charge and spin",
    )
    args = ap.parse_args()

    if args.task != "omol":
        print(
            f"warning: task '{args.task}' ignores atoms.info charge and spin, "
            "so the Ln(3+) spin state will not be represented\n"
        )
    common.run(f"{args.model}-{args.task}", make_calc, args)


if __name__ == "__main__":
    main()
