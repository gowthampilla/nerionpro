from pydantic import BaseModel
from typing import Optional, List, Dict

class AgentAction(BaseModel):
    agent_id: str
    action_type: str
    payload: str
    context_files: Optional[List[str]] = []
    user_api_key: str  # <--- THE BYOK REQUIREMENT

class RiskEvaluation(BaseModel):
    risk_score: int
    risk_level: str
    decision: str
    reason: str
    simulation_result: Optional[Dict] = None