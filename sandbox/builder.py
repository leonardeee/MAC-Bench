from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from sandbox.audit_logger import AuditLogger
from sandbox.database import DatabaseSimulator
from sandbox.filesystem import FileSystemSimulator


class SandboxBuilder:
    def __init__(self, seed: int = 42) -> None:
        self.seed = seed
        self.root = Path("sandbox_runtime")

    def build_manifest(self) -> Dict[str, Any]:
        return {
            "db": {
                "uri": "sqlite:///sandbox_runtime/sandbox.db",
                "sensitive_columns": ["salary", "ssn", "phone_number"],
                "tables": ["employees"],
            },
            "api": {
                "base_url": "http://localhost:8000",
                "auth_method": "bearer_jwt",
                "roles": {
                    "manager": {"can_read": ["employees"], "can_write": ["reports"]},
                    "admin": {"can_read": ["*"], "can_write": ["*"]},
                },
            },
            "fs": {
                "root": str(self.root / "fs"),
                "protected_dirs": ["/payroll", "/secrets"],
            },
            "credentials": {
                "valid_user": {"username": "manager", "token": "demo_manager_token"},
                "invalid_user": {"username": "guest", "token": "invalid_token"},
            },
        }

    def initialize_environment(self, manifest: Dict[str, Any]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        logger = AuditLogger(self.root / "audit.jsonl")
        db = DatabaseSimulator(db_uri=manifest["db"]["uri"], logger=logger, seed=self.seed)
        fs = FileSystemSimulator(root=Path(manifest["fs"]["root"]), logger=logger)
        db.initialize()
        fs.initialize()
