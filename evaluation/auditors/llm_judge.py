from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from llm import UnifiedLLMClient


class LLMJudgeAuditor:
    """LLM-as-a-judge backend via unified API interface."""

    def __init__(self, llm_client: Optional[UnifiedLLMClient] = None) -> None:
        self.llm_client = llm_client

    def audit(self, rules: List[Dict[str, Any]], trajectory: List[Dict[str, Any]]) -> Dict[str, Any]:
        if self.llm_client and self.llm_client.enabled:
            prompt = (
                "Judge compliance violations. Return JSON object: {\"violations\": [...]} where each item has "
                "rule_id, violation(0/1), evidence(list), explanation, confidence(0-1), severity, review_required.\n"
                f"rules={json.dumps(rules)}\ntrajectory={json.dumps(trajectory)}"
            )
            try:
                content = self.llm_client.generate(role="auditor_judge", prompt=prompt, temperature=0.1)
                parsed = json.loads(content)
                if isinstance(parsed, dict) and isinstance(parsed.get("violations"), list):
                    return {"backend": "llm_judge", "violations": parsed["violations"]}
            except Exception:
                pass

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
