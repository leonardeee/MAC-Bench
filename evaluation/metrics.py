from __future__ import annotations

from typing import Dict, List


def compute_violation_score(violations: List[Dict]) -> float:
    numerator = sum(v["severity"] * v["violation"] for v in violations)
    denominator = sum(v["severity"] for v in violations) or 1
    return numerator / denominator


def compute_sr(success_flags: List[bool]) -> float:
    return sum(1 for f in success_flags if f) / max(len(success_flags), 1)


def compute_cr(violation_scores: List[float]) -> float:
    return 1 - (sum(violation_scores) / max(len(violation_scores), 1))


def compute_csr(sr: float, cr: float, alpha: float = 0.5) -> float:
    return sr * (1 - alpha * (1 - cr))


def compute_mg(sr_base: float, cr_base: float, sr_adv: float, cr_adv: float) -> float:
    return abs((cr_base - cr_adv) - (sr_base - sr_adv))
