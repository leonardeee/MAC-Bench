from __future__ import annotations

import csv
from pathlib import Path


if __name__ == "__main__":
    metrics_path = Path("results/metrics_summary.csv")
    if not metrics_path.exists():
        raise SystemExit("metrics_summary.csv not found. Run scripts/run_benchmark.py first.")

    with metrics_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    latest = rows[-1]
    print("Latest metrics")
    for key, value in latest.items():
        print(f"- {key}: {value}")
