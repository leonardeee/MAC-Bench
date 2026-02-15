from __future__ import annotations

import random
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List

from sandbox.audit_logger import AuditLogger


class DatabaseSimulator:
    def __init__(self, db_uri: str, logger: AuditLogger, seed: int = 42) -> None:
        if db_uri.startswith("sqlite:///"):
            db_path = db_uri.replace("sqlite:///", "", 1)
        else:
            db_path = db_uri
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logger
        self.rng = random.Random(seed)

    def initialize(self) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("DROP TABLE IF EXISTS employees")
            conn.execute(
                "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER, email TEXT)"
            )
            rows = [
                (i, f"Employee-{i}", "X", 50000 + i * 500, f"user{i}@example.com")
                for i in range(1, 31)
            ]
            conn.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", rows)
            conn.commit()
        finally:
            conn.close()

    def query(self, sql: str, episode_id: str, agent: str) -> List[Dict[str, Any]]:
        latency_ms = self.rng.randint(50, 300)
        time.sleep(latency_ms / 1000.0)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.execute(sql)
            rows = [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

        self.logger.emit(
            episode_id=episode_id,
            agent=agent,
            tool="db.query",
            args={"sql": sql},
            result={"status": "success", "rows": len(rows)},
            meta={"latency_ms": latency_ms, "resource": "db.employees"},
        )
        return rows
