from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Optional
from urllib import error, request


@dataclass
class UnifiedLLMConfig:
    """OpenAI-compatible API configuration shared by all pipeline roles."""

    base_url: str = ""
    api_key: str = ""
    timeout_s: int = 60
    default_model: str = ""
    role_models: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "UnifiedLLMConfig":
        role_models = {
            "analyst": os.getenv("MAC_BENCH_MODEL_ANALYST", ""),
            "architect": os.getenv("MAC_BENCH_MODEL_ARCHITECT", ""),
            "test_subject": os.getenv("MAC_BENCH_MODEL_TEST_SUBJECT", ""),
            "auditor_judge": os.getenv("MAC_BENCH_MODEL_AUDITOR_JUDGE", ""),
        }
        return cls(
            base_url=os.getenv("MAC_BENCH_API_BASE_URL", "").rstrip("/"),
            api_key=os.getenv("MAC_BENCH_API_KEY", ""),
            timeout_s=int(os.getenv("MAC_BENCH_API_TIMEOUT_S", "60")),
            default_model=os.getenv("MAC_BENCH_MODEL_DEFAULT", ""),
            role_models={k: v for k, v in role_models.items() if v},
        )


class UnifiedLLMClient:
    def __init__(self, config: Optional[UnifiedLLMConfig] = None) -> None:
        self.config = config or UnifiedLLMConfig.from_env()

    @property
    def enabled(self) -> bool:
        return bool(self.config.base_url and self.config.api_key)

    def model_for_role(self, role: str) -> str:
        return self.config.role_models.get(role, self.config.default_model)

    def generate(
        self,
        role: str,
        prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        temperature: float = 0.2,
    ) -> str:
        if not self.enabled:
            raise RuntimeError("Unified LLM API is disabled. Missing MAC_BENCH_API_BASE_URL or MAC_BENCH_API_KEY.")

        model = self.model_for_role(role)
        if not model:
            raise RuntimeError(f"No model configured for role '{role}'.")

        payload = {
            "model": model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        req = request.Request(
            url=f"{self.config.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.config.timeout_s) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"LLM API HTTP error: {exc.code} {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"LLM API connection error: {exc.reason}") from exc

        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError(f"LLM API returned no choices: {data}")
        content = choices[0].get("message", {}).get("content", "")
        if not content:
            raise RuntimeError(f"LLM API returned empty content: {data}")
        return content
