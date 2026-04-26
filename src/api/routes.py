from fastapi import APIRouter
from .schemas import AgentAction, RiskEvaluation
from engine.llm import evaluate_with_llm
from simulator.sandbox import run_in_sandbox

router = APIRouter()

def enforce_policy(level):
    return "ALLOW" if level == "LOW" else "BLOCK"

@router.post("/evaluate", response_model=RiskEvaluation)
async def evaluate_action(action: AgentAction):
    
    # 1. Evaluate with BYOK
    llm_decision = evaluate_with_llm(action.action_type, action.payload, action.user_api_key)
    
    score = llm_decision.get("risk_score", 0)
    level = llm_decision.get("risk_level", "LOW")
    
    # 2. Run Sandbox if Risk > LOW
    simulation = None
    if level != "LOW":
        simulation = run_in_sandbox(action.payload, action.context_files)
    
    # 3. Final Decision
    decision = enforce_policy(level)
    final_reason = llm_decision.get("reason", "")
    
    if simulation:
        if "CRITICAL" in simulation.get("impact_report", ""):
            final_reason = f"🚨 {simulation['impact_report']} | {final_reason}"
        else:
            final_reason += f" | Sandbox: {simulation['observation']}"
    
    return RiskEvaluation(
        risk_score=score,
        risk_level=level,
        decision=decision,
        reason=final_reason,
        simulation_result=simulation
    )