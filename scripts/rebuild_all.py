"""
One-command reproduction of the Phase 4 analysis outputs and manuscript tables/figures.

Runs the full regeneration chain in order and then the test suite:
    1. build_phase4_tables.py          -> master mutation table (+ template-residue columns) + contrast
    2. build_phase4_analysis.py        -> permutation summary (all + non_core_only) + non-core screen
    3. build_review_driven_outputs.py  -> mechanism annotations + manuscript tables 1-3 + figures 1-4
    4. pytest                          -> confirm everything is consistent

This does NOT recompute the per-family structural metric CSVs (*_distance_sasa.csv), which need
ChimeraX (PPO/ALS/ACCase) or the pure-Python fallback (EPSPS); those change only when a structure or
active-site core changes. Everything downstream of the metric CSVs is regenerated here from committed
inputs, so a clean clone reproduces all pooled tables and figures with:  python scripts/rebuild_all.py
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    [sys.executable, "scripts/build_phase4_tables.py"],
    [sys.executable, "scripts/build_phase4_analysis.py"],
    [sys.executable, "scripts/build_review_driven_outputs.py"],
    [sys.executable, "scripts/build_resistance_zone_figure.py"],
    [sys.executable, "-m", "pytest", "-q"],
]


def main() -> int:
    for step in STEPS:
        printable = " ".join(step[1:])
        print(f"\n=== running: {printable} ===", flush=True)
        result = subprocess.run(step, cwd=REPO_ROOT)
        if result.returncode != 0:
            print(f"FAILED at: {printable} (exit {result.returncode})", file=sys.stderr)
            return result.returncode
    print("\nAll Phase 4 outputs regenerated and tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
