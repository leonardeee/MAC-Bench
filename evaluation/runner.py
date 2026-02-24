from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

from llm import UnifiedLLMClient

from agents.auditor import ComplianceAuditorAgent
from agents.test_subjects.autogen_runner import AutoGenRunner
from evaluation.metrics import compute_cr, compute_csr, compute_mg, compute_sr, compute_violation_score
from sandbox.audit_logger import AuditLogger
from sandbox.builder import SandboxBuilder
from sandbox.database import DatabaseSimulator
from sandbox.filesystem import FileSystemSimulator


class BenchmarkRunner:
    def __init__(self, seed: int = 42, llm_client: Optional[UnifiedLLMClient] = None) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.llm_client = llm_client

    def _simulate_actions(
        self,
        episode_id: str,
        framework_output: Dict[str, Any],
        db: DatabaseSimulator,
        fs: FileSystemSimulator,
        logger: AuditLogger,
    ) -> None:
        for action in framework_output["actions"]:
            tool = action["tool"]
            args = action["args"]
            if tool == "db.query":
                db.query(args["sql"], episode_id=episode_id, agent=framework_output["framework"])
            elif tool == "fs.read":
                fs.read(args["path"], episode_id=episode_id, agent=framework_output["framework"])
            elif tool == "api.call":
                logger.emit(
                    episode_id=episode_id,
                    agent=framework_output["framework"],
                    tool="api.call",
                    args=args,
                    result={"status": "success", "code": 200},
                    meta={"resource": args.get("endpoint", "unknown"), "auth": args.get("auth", "")},
                )

    def run(
        self,
        rules_path: Path,
        scenarios_path: Path,
        episodes_output: Path,
        violations_output: Path,
        max_episodes: int = 5,
    ) -> Dict[str, float]:
        rules = json.loads(rules_path.read_text(encoding="utf-8"))
        scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))[:max_episodes]

        builder = SandboxBuilder(seed=self.seed)
        manifest = builder.build_manifest()
        builder.initialize_environment(manifest)

        runtime_root = Path("sandbox_runtime")
        logger = AuditLogger(runtime_root / "audit.jsonl")
        db = DatabaseSimulator(manifest["db"]["uri"], logger=logger, seed=self.seed)
        db.initialize()
        fs = FileSystemSimulator(root=Path(manifest["fs"]["root"]), logger=logger)
        fs.initialize()

        runner = AutoGenRunner(llm_client=self.llm_client)
        auditor = ComplianceAuditorAgent(llm_client=self.llm_client)

        success_flags: List[bool] = []
        violation_scores: List[float] = []
        episodes_output.parent.mkdir(parents=True, exist_ok=True)
        episodes_output.write_text("", encoding="utf-8")

        for i, scenario in enumerate(scenarios, start=1):
            episode_id = f"ep-{i:05d}"
            framework_output = runner.run_episode(scenario)
            self._simulate_actions(episode_id, framework_output, db, fs, logger)

            trajectory_path = runtime_root / "audit.jsonl"
            audit_report = auditor.run(rules_path=rules_path, trajectory_path=trajectory_path, backend="deterministic")
            score = compute_violation_score(audit_report["violations"])

            success_flags.append(framework_output["success"])
            violation_scores.append(score)

            with episodes_output.open("a", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        {
                            "episode_id": episode_id,
                            "scenario_id": scenario["scenario_id"],
                            "framework": framework_output["framework"],
                            "success": framework_output["success"],
                            "violation_score": score,
                        }
                    )
                    + "\n"
                )

        violations_output.write_text(json.dumps(audit_report, indent=2), encoding="utf-8")

        sr = compute_sr(success_flags)
        cr = compute_cr(violation_scores)
        csr = compute_csr(sr, cr, alpha=0.7)
        mg = compute_mg(sr_base=sr, cr_base=cr, sr_adv=max(0.0, sr - 0.1), cr_adv=max(0.0, cr - 0.2))

        return {"SR": sr, "CR": cr, "CSR": csr, "MG": mg}
