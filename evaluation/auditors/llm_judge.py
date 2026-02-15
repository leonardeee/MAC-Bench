from __future__ import annotations

from typing import Any, Dict, List


class LLMJudgeAuditor:
    """Placeholder backend for provider-specific LLM-as-a-judge integration."""

    def audit(self, rules: List[Dict[str, Any]], trajectory: List[Dict[str, Any]]) -> Dict[str, Any]:
        violations = [
            {
                "rule_id": r["id"],
                "violation": 0,
                "evidence": [],
                "explanation": "LLM judge backend placeholder returned no violation by default.",
                "confidence": 0.5,
                "severity": r["severity"],
                "review_required": True,
            }
            for r in rules
        ]
        return {"backend": "llm_judge", "violations": violations}
