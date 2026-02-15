from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evaluation.serv_pipeline import SERVPipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=5)
    args = parser.parse_args()

    metrics = SERVPipeline(seed=42).run(episodes=args.episodes)
    Path("results/metrics_summary.csv").write_text(
        "SR,CR,CSR,MG\n"
        f"{metrics['SR']:.4f},{metrics['CR']:.4f},{metrics['CSR']:.4f},{metrics['MG']:.4f}\n",
        encoding="utf-8",
    )
    print(metrics)
