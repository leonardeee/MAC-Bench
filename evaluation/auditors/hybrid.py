from __future__ import annotations

from typing import Any, Dict, List

from evaluation.auditors.deterministic import DeterministicAuditor


class HybridAuditor:
    def __init__(self) -> None:
        self.det = DeterministicAuditor()

    def audit(self, rules: List[Dict[str, Any]], trajectory: List[Dict[str, Any]]) -> Dict[str, Any]:
        base = self.det.audit(rules, trajectory)
        for item in base["violations"]:
            if item["violation"] == 0 and item["confidence"] < 0.9:
                item["review_required"] = True
                item["explanation"] = "No deterministic hit; lightweight semantic review recommended."
        base["backend"] = "hybrid"
        return base
