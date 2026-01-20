from typing import Dict, List

from pydantic import BaseModel


class ComplianceSeed(BaseModel):
    id: str
    domain: str
    rule_content: str
    risk_level: str


class ScenarioSpec(BaseModel):
    seed_id: str
    scenario_id: str
    story_background: str
    user_instruction: str
    pressure_tactics: List[str]
    environment_requirements: Dict[str, str]


class EnvironmentBundle(BaseModel):
    scenario_id: str
    file_system: Dict[str, str]
    setup_command: str
