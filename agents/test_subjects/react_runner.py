from __future__ import annotations

from typing import Any, Dict


class ReActRunner:
    framework_name = "ReAct"

    def run_episode(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "framework": self.framework_name,
            "success": scenario.get("intensity", 0) < 5,
            "actions": [
                {"tool": "db.query", "args": {"sql": "SELECT * FROM employees"}},
            ],
            "final_answer": f"Processed scenario {scenario['scenario_id']}",
        }
