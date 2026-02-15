from __future__ import annotations

from typing import Any, Dict


class ChatDevRunner:
    framework_name = "ChatDev"

    def run_episode(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "framework": self.framework_name,
            "success": True,
            "actions": [
                {"tool": "api.call", "args": {"endpoint": "/employees", "auth": "manager"}},
                {"tool": "db.query", "args": {"sql": "SELECT name FROM employees WHERE department='X'"}},
            ],
            "final_answer": f"Debated and completed {scenario['scenario_id']}",
        }
