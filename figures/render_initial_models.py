#!/usr/bin/env python3
"""OVITO renders of the 24 initial Ln(OH)3(H2O)128 models, composed into one labeled grid.

Layout: 6 rows (La → Lu) × 4 columns (box/droplet × PBC/non-PBC).
All panels share the same orthographic scale so cube vs droplet size is comparable.
Bulk water is translucent so the Ln ion and first shell remain visible.
"""
from __future__ import annotations

import argparse
import math
import os
import string
import sys
from pathlib import Path

# Headless Tachyon must not inherit a broken Qt/GL session.
os.environ.setdefault("QT_QPA_PLATFORM", os.environ.get("QT_QPA_PLATFORM", "offscreen"))

import numpy as np
from ovito.io import import_file
from ovito.modifiers import CreateBondsModifier
from ovito.vis import BondsVis, ParticlesVis, TachyonRenderer, Viewport
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
STRUCT = ROOT / "structures"
OUTDIR = Path(__file__).resolve().parent

METALS = ["La", "Nd", "Gd", "Dy", "Er", "Lu"]
CN = {"La": 9, "Nd": 9, "Gd": 9, "Dy": 8, "Er": 8, "Lu": 8}
VARIANTS = [
    ("box_pbc", "box / PBC"),
    ("box_nonpbc", "box / non-PBC"),
    ("droplet_pbc", "droplet / PBC"),
    ("droplet_nonpbc", "droplet / non-PBC"),
]

# Shared orthographic half-height (Å). Vertical field = 2 * FOV_A.
# Box diagonal projection ~22 Å; droplet span ~20 Å; margin for H and cell edges.
FOV_A = 14.6
# Slightly off-axis so a cube reads as a cube (not a [111] hexagon) and a
# droplet_pbc cell diagonal does not project as three lines through the ion.
CAMERA_DIR = np.array([0.92, 0.48, 0.32], dtype=float)

# Display radii (Å)
R_LN, R_OH, R_SHELL_O, R_BULK_O = 1.28, 0.58, 0.52, 0.40
R_SHELL_H, R_BULK_H = 0.18, 0.14

COLOR_LN = (0.95, 0.72, 0.12)
COLOR_OH = (1.00, 0.48, 0.05)
COLOR_SHELL_O = (0.86, 0.08, 0.08)
COLOR_BULK_O = (1.00, 0.38, 0.38)
COLOR_H = (0.96, 0.96, 0.98)
COLOR_CELL = (0.18, 0.18, 0.22)

T_BULK_O, T_BULK_H = 0.42, 0.55
OH_CUTOFF = 1.18
LN_O_BOND = 2.90
OH_BOND = 1.22


def _fonts(caption: int, title: int, small: int):
    regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    return (
        ImageFont.truetype(bold, title),
        ImageFont.truetype(bold, caption),
        ImageFont.truetype(regular, caption),
        ImageFont.truetype(regular, small),
        ImageFont.truetype(bold, small + 2),
    )


def _camera_basis():
    d = CAMERA_DIR / np.linalg.norm(CAMERA_DIR)
    up = np.array([0.0, 0.0, 1.0])
    up = up - np.dot(up, d) * d
    n = np.linalg.norm(up)
    if n < 1e-8:
        up = np.array([0.0, 1.0, 0.0])
        up = up - np.dot(up, d) * d
        n = np.linalg.norm(up)
    up /= n
    return d, up


def _classify(types: np.ndarray, pos: np.ndarray, metal: str):
    """Return per-atom role: ln / oh / shell_ow / bulk_ow / shell_h / bulk_h."""
    names = np.asarray(types)
    ln_i = np.flatnonzero(names == metal)
    o_i = np.flatnonzero(names == "O")
    h_i = np.flatnonzero(names == "H")
    ln = pos[ln_i[0]]
    d_ln = np.linalg.norm(pos[o_i] - ln, axis=1)
    order = np.argsort(d_ln)
    shell = set(o_i[order[: CN[metal]]].tolist())
    roles = np.empty(len(names), dtype=object)
    oh = set()
    for i in o_i:
        n_h = int(np.sum(np.linalg.norm(pos[h_i] - pos[i], axis=1) < OH_CUTOFF))
        if n_h <= 1:
            roles[i] = "oh"
            oh.add(i)
        elif i in shell:
            roles[i] = "shell_ow"
        else:
            roles[i] = "bulk_ow"
    first_o = shell | oh
    for i in h_i:
        d = np.linalg.norm(pos[o_i] - pos[i], axis=1)
        nearest = int(o_i[int(np.argmin(d))])
        roles[i] = "shell_h" if nearest in first_o else "bulk_h"
    for i in ln_i:
        roles[i] = "ln"
    return roles


def _style_modifier(metal: str, show_cell: bool):
    def modify(frame, data):  # noqa: ARG001
        pts = data.particles_
        type_ids = np.asarray(pts.particle_types)
        id_to_name = {t.id: t.name for t in pts.particle_types.types}
        names = np.array([id_to_name[int(i)] for i in type_ids])
        pos = np.asarray(pts.positions)
        roles = _classify(names, pos, metal)
        n = len(roles)
        color = np.zeros((n, 3), dtype=float)
        radius = np.zeros(n, dtype=float)
        transp = np.zeros(n, dtype=float)
        lut = {
            "ln": (COLOR_LN, R_LN, 0.0),
            "oh": (COLOR_OH, R_OH, 0.0),
            "shell_ow": (COLOR_SHELL_O, R_SHELL_O, 0.0),
            "bulk_ow": (COLOR_BULK_O, R_BULK_O, T_BULK_O),
            "shell_h": (COLOR_H, R_SHELL_H, 0.08),
            "bulk_h": (COLOR_H, R_BULK_H, T_BULK_H),
        }
        for i, role in enumerate(roles):
            c, r, t = lut[role]
            color[i] = c
            radius[i] = r
            transp[i] = t
        pts.create_property("Color", data=color)
        pts.create_property("Radius", data=radius)
        pts.create_property("Transparency", data=transp)
        pts.vis.shape = ParticlesVis.Shape.Sphere
        if pts.bonds is not None:
            pts.bonds.vis.enabled = True
            pts.bonds.vis.width = 0.14
            pts.bonds.vis.use_particle_colors = True
            pts.bonds.vis.shading = BondsVis.Shading.Normal
        if data.cell is not None:
            data.cell_.vis.enabled = bool(show_cell)
            data.cell_.vis.render_cell = bool(show_cell)
            data.cell_.vis.rendering_color = COLOR_CELL
            data.cell_.vis.line_width = 0.10

    return modify


def _build_renderer(kind: str):
    k = kind.lower().strip()
    if k in {"gpu", "cuda", "rtx", "anari"}:
        from ovito.vis import AnariRenderer

        return "anari", AnariRenderer(samples_per_pixel=16, denoising_enabled=True)
    if k == "opengl":
        from ovito.vis import OpenGLRenderer

        return "opengl", OpenGLRenderer()
    return "tachyon", TachyonRenderer(
        antialiasing=True,
        antialiasing_samples=12,
        shadows=True,
        ambient_occlusion=True,
        ambient_occlusion_samples=12,
        direct_light_intensity=1.05,
        ambient_occlusion_brightness=0.75,
    )


def render_one(xyz: Path, metal: str, pbc: bool, png: Path, size: int, renderer_name: str) -> str:
    pipeline = import_file(str(xyz))
    bonds = CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise)
    bonds.set_pairwise_cutoff("O", "H", OH_BOND)
    bonds.set_pairwise_cutoff(metal, "O", LN_O_BOND)
    pipeline.modifiers.append(bonds)
    pipeline.modifiers.append(_style_modifier(metal, show_cell=pbc))
    pipeline.add_to_scene()
    try:
        data = pipeline.compute()
        pos = np.asarray(data.particles.positions)
        center = pos.mean(axis=0)
        direction, up = _camera_basis()
        vp = Viewport(type=Viewport.Type.Ortho)
        vp.fov = FOV_A
        vp.camera_dir = tuple(float(x) for x in direction)
        vp.camera_up = tuple(float(x) for x in up)
        vp.camera_pos = tuple(float(x) for x in (center - direction * 90.0))
        used = renderer_name
        try:
            used, renderer = _build_renderer(renderer_name)
            vp.render_image(
                size=(size, size),
                filename=str(png),
                renderer=renderer,
                background=(1.0, 1.0, 1.0),
            )
        except RuntimeError as exc:
            msg = str(exc).lower()
            if renderer_name != "tachyon" and any(
                k in msg for k in ("anari", "visrtx", "opengl", "initialization")
            ):
                used, renderer = _build_renderer("tachyon")
                vp.render_image(
                    size=(size, size),
                    filename=str(png),
                    renderer=renderer,
                    background=(1.0, 1.0, 1.0),
                )
            else:
                raise
        return used
    finally:
        pipeline.remove_from_scene()


def _text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def compose_grid(panel_dir: Path, out: Path, panel: int) -> None:
    font_title, font_cap_b, font_cap, font_small, font_letter = _fonts(22, 36, 16)
    nrows, ncols = len(METALS), len(VARIANTS)
    margin = 36
    title_h = 78
    col_h = 44
    row_w = 168
    cap_h = 34
    gap = 14
    legend_h = 96
    cell_w, cell_h = panel, panel + cap_h
    width = margin + row_w + ncols * (cell_w + gap) - gap + margin
    height = margin + title_h + col_h + nrows * (cell_h + gap) - gap + legend_h + margin
    canvas = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    title = "Initial models   Ln³⁺  +  3 OH⁻  +  128 H₂O"
    tw, th = _text_size(draw, title, font_title)
    draw.text(((width - tw) / 2, margin + (title_h - th) / 2 - 6), title, fill=(20, 20, 20), font=font_title)
    subtitle = "same composition · four boundary-condition variants · identical scale"
    sw, sh = _text_size(draw, subtitle, font_small)
    draw.text(((width - sw) / 2, margin + title_h - sh - 8), subtitle, fill=(90, 90, 90), font=font_small)

    origin_x = margin + row_w
    origin_y = margin + title_h + col_h
    letters = list(string.ascii_lowercase)

    for j, (_, vlabel) in enumerate(VARIANTS):
        x = origin_x + j * (cell_w + gap)
        ww, hh = _text_size(draw, vlabel, font_cap_b)
        draw.text((x + (cell_w - ww) / 2, origin_y - col_h + (col_h - hh) / 2), vlabel, fill=(25, 25, 25), font=font_cap_b)

    k = 0
    for i, metal in enumerate(METALS):
        y = origin_y + i * (cell_h + gap)
        row = f"{metal}   (CN {CN[metal]})"
        ww, hh = _text_size(draw, row, font_cap_b)
        draw.text((margin + row_w - ww - 16, y + (panel - hh) / 2), row, fill=(25, 25, 25), font=font_cap_b)
        for j, (variant, vlabel) in enumerate(VARIANTS):
            x = origin_x + j * (cell_w + gap)
            png = panel_dir / f"{metal}_{variant}.png"
            img = Image.open(png).convert("RGB").resize((panel, panel), Image.Resampling.LANCZOS)
            canvas.paste(img, (x, y))
            draw.rectangle([x, y, x + panel - 1, y + panel - 1], outline=(40, 40, 40), width=1)
            letter = f"({letters[k]})"
            cap = f"{letter}  {metal}  ·  {vlabel}"
            cw, ch = _text_size(draw, cap, font_cap)
            draw.text((x + (cell_w - cw) / 2, y + panel + (cap_h - ch) / 2 - 2), cap, fill=(30, 30, 30), font=font_cap)
            # letter badge on the image
            lw, lh = _text_size(draw, letter, font_letter)
            bx, by = x + 10, y + 8
            draw.rounded_rectangle(
                [bx - 4, by - 2, bx + lw + 6, by + lh + 4],
                radius=4,
                fill=(255, 255, 255),
                outline=(60, 60, 60),
            )
            draw.text((bx, by), letter, fill=(20, 20, 20), font=font_letter)
            k += 1

    # Legend + scale bar
    ly = origin_y + nrows * (cell_h + gap) - gap + 18
    swatches = [
        (COLOR_LN, "Ln³⁺"),
        (COLOR_OH, "OH⁻  (1st shell)"),
        (COLOR_SHELL_O, "H₂O  (1st shell)"),
        (COLOR_BULK_O, "H₂O  (bulk, translucent)"),
        (COLOR_H, "H"),
    ]
    lx = margin + row_w
    r = 11
    for col, label in swatches:
        rgb = tuple(int(255 * c) for c in col)
        draw.ellipse([lx, ly + 8, lx + 2 * r, ly + 8 + 2 * r], fill=rgb, outline=(40, 40, 40))
        draw.text((lx + 2 * r + 8, ly + 10), label, fill=(30, 30, 30), font=font_small)
        lx += 2 * r + 8 + _text_size(draw, label, font_small)[0] + 28

    # 5 Å scale bar. Panel pixels map as: 2*FOV_A Å = panel px (vertical).
    bar_A = 5.0
    bar_px = int(round(bar_A / (2.0 * FOV_A) * panel))
    bx = width - margin - bar_px - 8
    by = ly + 28
    draw.line([(bx, by), (bx + bar_px, by)], fill=(20, 20, 20), width=3)
    draw.line([(bx, by - 6), (bx, by + 6)], fill=(20, 20, 20), width=2)
    draw.line([(bx + bar_px, by - 6), (bx + bar_px, by + 6)], fill=(20, 20, 20), width=2)
    sl = "5 Å"
    sww, shh = _text_size(draw, sl, font_small)
    draw.text((bx + (bar_px - sww) / 2, by + 8), sl, fill=(30, 30, 30), font=font_small)

    canvas.save(out, dpi=(300, 300))
    print(f"Wrote {out}  ({width}×{height} px)")


def iter_jobs(only: str | None):
    for metal in METALS:
        for variant, label in VARIANTS:
            if only and only not in f"{metal}_{variant}" and only not in metal:
                continue
            xyz = STRUCT / variant / f"{metal}-3OH-128H2O_{variant}.xyz"
            yield metal, variant, label, xyz, variant.endswith("_pbc")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel-size", type=int, default=720)
    ap.add_argument("--renderer", default="tachyon", help="tachyon | anari | opengl")
    ap.add_argument("--only", default=None, help="Substring filter, e.g. Dy or box_pbc")
    ap.add_argument("--skip-render", action="store_true")
    args = ap.parse_args()

    panel_dir = OUTDIR / "panels"
    panel_dir.mkdir(parents=True, exist_ok=True)
    jobs = list(iter_jobs(args.only))
    if not jobs:
        raise SystemExit(f"no jobs matched --only {args.only!r}")

    used = args.renderer
    if not args.skip_render:
        for n, (metal, variant, label, xyz, pbc) in enumerate(jobs, 1):
            if not xyz.is_file():
                raise FileNotFoundError(xyz)
            png = panel_dir / f"{metal}_{variant}.png"
            print(f"[{n}/{len(jobs)}] {metal} {label}  ←  {xyz.name}", flush=True)
            show_cell = variant == "box_pbc"
            used = render_one(xyz, metal, show_cell, png, args.panel_size, args.renderer)
        print(f"renderer: {used}", flush=True)

    if args.only is None:
        compose_grid(panel_dir, OUTDIR / "initial_models_grid.png", args.panel_size)
    else:
        print("skip full grid (--only set); panels are in", panel_dir)


if __name__ == "__main__":
    main()
