#!/usr/bin/env python3
"""Short-queue speed test of UMA omol: default vs turbo.

Turbo (merge_mole + torch.compile) only stays on the fast path when composition,
task, charge and spin are all fixed.  This bench therefore uses a single metal
(default La: closed shell, 2S+1 = 1) and its four boundary-condition variants
as the queue, then repeats the same-composition evaluations after warmup.

Best-performance knobs:
  - uma-s-1p2 (small, MD-oriented)
  - inference_settings="turbo"
  - CUDA, TF32 allowed
  - one composition / charge / spin for the whole timed loop
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mlip"))
sys.path.insert(0, str(ROOT / "build"))

from common import load_system, warn_if_periodic  # noqa: E402


def _cuda_perf_flags():
    import torch

    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    torch.set_float32_matmul_precision("high")
    if torch.cuda.is_available():
        torch.cuda.set_device(0)
        torch.cuda.empty_cache()


def _make_calc(model, settings, task, device):
    from fairchem.core import FAIRChemCalculator, pretrained_mlip

    predictor = pretrained_mlip.get_predict_unit(
        model, inference_settings=settings, device=device
    )
    return FAIRChemCalculator(predictor, task_name=task)


def _eval(atoms, rng):
    # ASE caches energy/forces on an unchanged Atoms object.  A 1e-4 A jitter
    # is enough to force a real forward pass while staying on the same compiled
    # graph (composition / cell / PBC unchanged).
    atoms.positions = atoms.positions + rng.normal(scale=1e-4, size=atoms.positions.shape)
    e = float(atoms.get_potential_energy())
    f = atoms.get_forces()
    return e, float((f**2).sum() ** 0.5)


def _sync():
    import torch

    if torch.cuda.is_available():
        torch.cuda.synchronize()


def _time_loop(atoms_list, n_repeat, label, rng):
    times = []
    last = None
    for i in range(n_repeat):
        atoms = atoms_list[i % len(atoms_list)]
        _sync()
        t0 = time.perf_counter()
        last = _eval(atoms, rng)
        _sync()
        dt = time.perf_counter() - t0
        times.append(dt)
        print(f"    {label}  step {i+1:3d}/{n_repeat}  {dt*1e3:8.1f} ms  E={last[0]:.4f} eV")
    return times, last


def ns_per_day(seconds_per_step, dt_fs=1.0):
    steps_per_ns = 1000.0 / dt_fs * 1e6 / 1000.0  # 1e6 fs / dt_fs
    return 86400.0 / (seconds_per_step * (1e6 / dt_fs))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(ROOT / "structures"))
    ap.add_argument("--metal", default="La", help="fixed composition for turbo")
    ap.add_argument("--model", default="uma-s-1p2")
    ap.add_argument("--task", default="omol")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--warmup", type=int, default=3)
    ap.add_argument("--repeat", type=int, default=12, help="timed steps after warmup")
    ap.add_argument("--settings", nargs="+", default=["default", "turbo"])
    ap.add_argument("--out", default=str(ROOT / "reports" / "uma_turbo_bench.json"))
    args = ap.parse_args()

    import numpy as np
    import torch

    rng = np.random.default_rng(20260901)
    _cuda_perf_flags()
    print(f"torch {torch.__version__}  cuda {torch.version.cuda}  {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'}")
    print(f"model {args.model}  task {args.task}  metal {args.metal}  settings {args.settings}\n")

    # Turbo's fast path is for fixed composition/charge/spin *and* a stable
    # graph (MD-like).  Cycling box vs droplet or PBC vs vacuum forces a
    # recompile / fallback, so the timed loop stays on one structure.
    variant = "droplet_nonpbc"
    path = Path(args.root) / variant / f"{args.metal}-3OH-128H2O_{variant}.xyz"
    atoms = load_system(path)
    frames = [atoms]
    print(
        f"  timed structure  {path.relative_to(args.root)}  "
        f"{len(atoms)} atoms  charge {atoms.info['charge']}  2S+1={atoms.info['spin']}"
    )
    print()

    report = {
        "model": args.model,
        "task": args.task,
        "metal": args.metal,
        "n_atoms": len(frames[0]),
        "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "torch": torch.__version__,
        "settings": {},
    }

    for settings in args.settings:
        print(f"=== {settings} ===")
        frames = [load_system(path)]
        t_load = time.perf_counter()
        calc = _make_calc(args.model, settings, args.task, args.device)
        load_s = time.perf_counter() - t_load
        print(f"  loaded in {load_s:.1f} s")

        for atoms in frames:
            atoms.calc = calc

        print(f"  warmup ({args.warmup} steps, includes compile on turbo) ...")
        t_w = time.perf_counter()
        warm, _ = _time_loop(frames, args.warmup, f"{settings}/warm", rng)
        compile_s = time.perf_counter() - t_w
        print(f"  warmup wall {compile_s:.1f} s")

        print(f"  timed queue ({args.repeat} steps on the same {args.metal} {variant}) ...")
        times, last = _time_loop(frames, args.repeat, f"{settings}/run", rng)
        # drop the slowest as leftover compile/cache miss if any
        core = sorted(times)[1:-1] if len(times) >= 6 else times
        med = statistics.median(times)
        mean = statistics.mean(core)
        qps = 1.0 / med
        entry = {
            "load_s": load_s,
            "warmup_s": compile_s,
            "warmup_ms": [round(x * 1e3, 2) for x in warm],
            "step_ms": [round(x * 1e3, 2) for x in times],
            "median_ms": round(med * 1e3, 2),
            "mean_ms_trim": round(mean * 1e3, 2),
            "qps": round(qps, 2),
            "ns_per_day_1fs": round(ns_per_day(med, 1.0), 3),
            "last_energy_eV": last[0] if last else None,
        }
        report["settings"][settings] = entry
        print(
            f"  median {entry['median_ms']:.1f} ms/step  "
            f"({entry['qps']:.2f} eval/s,  {entry['ns_per_day_1fs']:.2f} ns/day @ 1 fs)\n"
        )
        del calc
        for atoms in frames:
            atoms.calc = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    if set(args.settings) >= {"default", "turbo"}:
        d = report["settings"]["default"]["median_ms"]
        t = report["settings"]["turbo"]["median_ms"]
        report["speedup_turbo_over_default"] = round(d / t, 2) if t else None
        print(f"turbo / default speedup: {report['speedup_turbo_over_default']}x  "
              f"({d:.1f} -> {t:.1f} ms)")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2))
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
