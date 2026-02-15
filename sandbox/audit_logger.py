from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class AuditLogger:
    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(
        self,
        episode_id: str,
        agent: str,
        tool: str,
        args: Dict[str, Any],
        result: Dict[str, Any],
        meta: Dict[str, Any],
    ) -> None:
        digest = hashlib.sha256(json.dumps(result, sort_keys=True).encode("utf-8")).hexdigest()[:12]
        event = {
            "t": datetime.now(timezone.utc).isoformat(),
            "episode_id": episode_id,
            "agent": agent,
            "tool": tool,
            "args": args,
            "result": {**result, "hash": digest},
            "meta": meta,
        }
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
