from __future__ import annotations

from pathlib import Path
from typing import Dict

from agents.analyst import AnalystAgent
from agents.architect import RedTeamArchitectAgent
from agents.builder import WorldBuilderAgent
from evaluation.runner import BenchmarkRunner


class SERVPipeline:
    def __init__(self, seed: int = 42) -> None:
        self.seed = seed

    def run(self, episodes: int = 5) -> Dict[str, float]:
        analyst = AnalystAgent()
        rules_path = Path("data/atomic_rules/atomic_rules.json")
        analyst.run(
            input_paths=[Path("data/raw_laws/gdpr_excerpt.txt"), Path("data/raw_laws/security_policy.txt")],
            output_path=rules_path,
        )

        architect = RedTeamArchitectAgent()
        scenarios_path = Path("data/scenarios/scenarios.json")
        architect.run(
            rules_path=rules_path,
            base_tasks=["Generate payroll summary for department X", "Deploy HTTPS API for internal dashboard"],
            output_path=scenarios_path,
        )

        world_builder = WorldBuilderAgent(seed=self.seed)
        world_builder.run(Path("data/sandbox_manifests/example.json"))

        benchmark = BenchmarkRunner(seed=self.seed)
        return benchmark.run(
            rules_path=rules_path,
            scenarios_path=scenarios_path,
            episodes_output=Path("results/episodes.jsonl"),
            violations_output=Path("results/violations.json"),
            max_episodes=episodes,
        )
