#!/usr/bin/env python3
"""Render an overview figure of the box and droplet models."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from ase.io import read

COLOURS = {"O": "#d94f4f", "H": "#e8e8e8"}
METAL_COLOUR = "#7b3fbf"


def panel(ax, path, title, metal):
    atoms = read(path, format="extxyz")
    symbols = np.array(atoms.get_chemical_symbols())
    colours = np.array(
        [METAL_COLOUR if s == metal else COLOURS.get(s, "#888888") for s in symbols]
    )
    order = np.argsort(atoms.positions[:, 1])  # crude depth sorting
    sizes = np.where(symbols == metal, 320.0, np.where(symbols == "O", 130.0, 45.0))

    p = atoms.positions[order]
    ax.scatter(
        p[:, 0],
        p[:, 2],
        s=sizes[order],
        c=colours[order],
        edgecolors="#2b2b2b",
        linewidths=0.4,
    )
    if atoms.pbc.all() and atoms.info["geometry"] == "box":
        L = atoms.cell.lengths()[0]
        ax.add_patch(
            plt.Rectangle(
                (0, 0), L, L, fill=False, ec="#1f77b4", lw=1.6, ls="--", zorder=5
            )
        )
    ax.set_title(title, fontsize=10)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="structures")
    ap.add_argument("--metals", nargs="*", default=["La", "Gd", "Lu"])
    ap.add_argument("--out", default="reports/overview.png")
    args = ap.parse_args()

    root = Path(args.root)
    variants = [
        ("box_pbc", "box, PBC (L = 15.78 A)"),
        ("droplet_nonpbc", "droplet, non-PBC (R = 9.8 A)"),
    ]
    fig, axes = plt.subplots(
        len(variants), len(args.metals), figsize=(4.1 * len(args.metals), 4.4 * len(variants))
    )
    axes = np.atleast_2d(axes)

    for i, (variant, label) in enumerate(variants):
        for j, metal in enumerate(args.metals):
            f = root / variant / f"{metal}-3OH-128H2O_{variant}.xyz"
            mult = read(f, format="extxyz").info["spin"]
            panel(axes[i, j], f, f"{metal}(3+)  2S+1 = {mult}\n{label}", metal)

    fig.suptitle(
        "Ln(3+) + 3 OH- + 128 H2O   (391 atoms, net charge 0)   purple = Ln, red = O, white = H",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=150)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
