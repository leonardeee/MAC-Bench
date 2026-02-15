from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from sandbox.builder import SandboxBuilder


class WorldBuilderAgent:
    """Creates runnable sandbox environments and emits manifests."""

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed

    def run(self, output_manifest_path: Path) -> Dict[str, Any]:
        builder = SandboxBuilder(seed=self.seed)
        manifest = builder.build_manifest()
        builder.initialize_environment(manifest)

        output_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        output_manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return manifest
