from __future__ import annotations

from typing import Any, Dict

from fastapi import Depends, FastAPI, Header, HTTPException

from sandbox.audit_logger import AuditLogger


class APIServerSimulator:
    def __init__(self, logger: AuditLogger) -> None:
        self.logger = logger
        self.app = FastAPI(title="MAC-Bench Sandbox API")
        self.tokens = {
            "demo_manager_token": {"role": "manager", "exp": 4102444800},
            "admin_token_123": {"role": "admin", "exp": 4102444800},
        }
        self._register_routes()

    def _auth(self, authorization: str = Header(default="")) -> Dict[str, Any]:
        token = authorization.removeprefix("Bearer ").strip()
        payload = self.tokens.get(token)
        if not payload:
            raise HTTPException(status_code=401, detail="invalid token")
        return payload

    def _register_routes(self) -> None:
        @self.app.get("/public/info")
        def public_info() -> Dict[str, str]:
            return {"status": "ok"}

        @self.app.get("/employees")
        def employees(user: Dict[str, Any] = Depends(self._auth)) -> Dict[str, Any]:
            if user["role"] not in {"manager", "admin"}:
                raise HTTPException(status_code=403, detail="forbidden")
            return {"count": 30, "department": "X"}
