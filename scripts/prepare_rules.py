from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.analyst import AnalystAgent


if __name__ == "__main__":
    analyst = AnalystAgent()
    rules = analyst.run(
        input_paths=[Path("data/raw_laws/gdpr_excerpt.txt"), Path("data/raw_laws/security_policy.txt")],
        output_path=Path("data/atomic_rules/atomic_rules.json"),
    )
    print(f"Prepared {len(rules)} rules.")
