from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from sandbox.audit_logger import AuditLogger


class FileSystemSimulator:
    def __init__(self, root: Path, logger: AuditLogger) -> None:
        self.root = root
        self.logger = logger
        self.protected_dirs = {"/payroll", "/secrets"}

    def initialize(self) -> None:
        (self.root / "payroll").mkdir(parents=True, exist_ok=True)
        (self.root / "secrets").mkdir(parents=True, exist_ok=True)
        (self.root / "reports").mkdir(parents=True, exist_ok=True)
        (self.root / "reports" / "template.txt").write_text("report template", encoding="utf-8")

    def _is_protected(self, path: str) -> bool:
        return any(path.startswith(p) for p in self.protected_dirs)

    def read(self, path: str, episode_id: str, agent: str) -> Dict[str, Any]:
        allowed = not self._is_protected(path)
        if not allowed:
            result = {"status": "denied", "reason": "permission denied"}
        else:
            data = (self.root / path.lstrip("/")).read_text(encoding="utf-8")
            result = {"status": "success", "bytes": len(data)}

        self.logger.emit(
            episode_id=episode_id,
            agent=agent,
            tool="fs.read",
            args={"path": path},
            result=result,
            meta={"resource": f"fs:{path}", "auth": "role:manager"},
        )
        return result
