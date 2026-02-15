from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class AtomicRule:
    id: str
    domain: str
    source: str
    cite: str
    scope: List[str]
    pre: str
    forbidden: List[str]
    required: List[str]
    severity: int


class AnalystAgent:
    """Converts policy text into process-oriented atomic rules."""

    def __init__(self, model_name: str = "deterministic-analyst") -> None:
        self.model_name = model_name

    def extract_rules_from_text(self, text: str, source: str) -> List[AtomicRule]:
        text_lower = text.lower()
        rules: List[AtomicRule] = []

        if "data minimization" in text_lower or "limited to what is necessary" in text_lower:
            rules.append(
                AtomicRule(
                    id=f"{source.upper()}-DATA-MIN-01",
                    domain="privacy",
                    source=source,
                    cite="Article 5(1)(c)",
                    scope=["db"],
                    pre="when exporting user data",
                    forbidden=["select columns beyond immediate need"],
                    required=["project only necessary columns", "apply row filters for minimization"],
                    severity=3,
                )
            )

        if "authentication" in text_lower or "token" in text_lower:
            rules.append(
                AtomicRule(
                    id=f"{source.upper()}-AUTH-01",
                    domain="code_sec",
                    source=source,
                    cite="Authentication policy clause",
                    scope=["api"],
                    pre="when accessing protected API endpoints",
                    forbidden=["accept expired or invalid tokens"],
                    required=["verify token signature", "check token expiration"],
                    severity=5,
                )
            )

        if "audit logging" in text_lower or "logs" in text_lower:
            rules.append(
                AtomicRule(
                    id=f"{source.upper()}-LOG-01",
                    domain="devops",
                    source=source,
                    cite="Audit retention clause",
                    scope=["fs", "api"],
                    pre="when performing maintenance",
                    forbidden=["clear system logs", "disable logging"],
                    required=["archive logs before deletion", "verify logging service is enabled"],
                    severity=3,
                )
            )

        return rules

    def run(self, input_paths: List[Path], output_path: Path) -> List[AtomicRule]:
        compiled: List[AtomicRule] = []
        for path in input_paths:
            text = path.read_text(encoding="utf-8")
            source = path.stem.upper()
            compiled.extend(self.extract_rules_from_text(text, source=source))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps([rule.__dict__ for rule in compiled], indent=2),
            encoding="utf-8",
        )
        return compiled
