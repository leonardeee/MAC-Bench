from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from evaluation.auditors.deterministic import DeterministicAuditor
from evaluation.auditors.hybrid import HybridAuditor
from evaluation.auditors.llm_judge import LLMJudgeAuditor


class ComplianceAuditorAgent:
    """Runs selected auditor backend over trajectory events and rules."""

    BACKENDS = {
        "deterministic": DeterministicAuditor,
        "hybrid": HybridAuditor,
        "llm_judge": LLMJudgeAuditor,
    }

    def run(self, rules_path: Path, trajectory_path: Path, backend: str = "deterministic") -> Dict[str, Any]:
        rules = json.loads(rules_path.read_text(encoding="utf-8"))
        trajectory = [json.loads(line) for line in trajectory_path.read_text(encoding="utf-8").splitlines() if line.strip()]

        auditor_cls = self.BACKENDS[backend]
        auditor = auditor_cls()
        return auditor.audit(rules=rules, trajectory=trajectory)
