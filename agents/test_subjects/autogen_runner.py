from __future__ import annotations

from typing import Any, Dict


class AutoGenRunner:
    framework_name = "AutoGen"

    def run_episode(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "framework": self.framework_name,
            "success": True,
            "actions": [
                {"tool": "api.call", "args": {"endpoint": "/employees", "auth": "manager"}},
                {"tool": "db.query", "args": {"sql": "SELECT name,department FROM employees"}},
            ],
            "final_answer": f"Completed scenario {scenario['scenario_id']}",
        }
