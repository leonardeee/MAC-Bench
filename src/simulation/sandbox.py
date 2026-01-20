import os

import docker

from src.schemas import EnvironmentBundle


class DockerSandbox:
    def __init__(self) -> None:
        self.client = docker.from_env()
        self.image = "python:3.10-slim"

    def run_simulation(self, env_bundle: EnvironmentBundle, agent_action_script: str) -> dict:
        host_path = f"/tmp/mac_bench/{env_bundle.scenario_id}"
        os.makedirs(host_path, exist_ok=True)

        for filename, content in env_bundle.file_system.items():
            with open(f"{host_path}/{filename}", "w", encoding="utf-8") as file_handle:
                file_handle.write(content)

        container = self.client.containers.run(
            self.image,
            command="/bin/bash",
            detach=True,
            tty=True,
            volumes={host_path: {"bind": "/workspace", "mode": "rw"}},
            working_dir="/workspace",
        )

        try:
            container.exec_run(f"bash -c '{env_bundle.setup_command}'")
            exec_result = container.exec_run("python3 agent_execution_logic.py")
            judge_result = container.exec_run("python3 check_script.py")

            return {
                "output": exec_result.output.decode(),
                "judge_log": judge_result.output.decode(),
                "exit_code": judge_result.exit_code,
            }
        finally:
            container.stop()
            container.remove()
