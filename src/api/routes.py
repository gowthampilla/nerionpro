from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import AgentAction, RiskEvaluation
from core.database import get_db
from models.trace import ActionTrace
from engine.llm import evaluate_with_llm
from engine.policy import enforce_policy
from simulator.sandbox import run_in_sandbox

router = APIRouter()

@router.post("/evaluate", response_model=RiskEvaluation)
async def evaluate_action(action: AgentAction, db: Session = Depends(get_db)):
    
    # THE FIX: We MUST pass action.user_api_key here
    llm_decision = evaluate_with_llm(action.action_type, action.payload, action.user_api_key)
    
    score = llm_decision.get("risk_score", 0)
    level = llm_decision.get("risk_level", "LOW")
    
    simulation = None
    if level != "LOW":
        simulation = run_in_sandbox(action.payload, action.context_files)
    
    decision = enforce_policy(level)
    
    final_reason = llm_decision.get("reason", "")
    if simulation:
        if "DELETED" in simulation.get("impact_report", ""):
            final_reason = f"🚨 {simulation['impact_report']} | {final_reason}"
        else:
            final_reason += f" | Sandbox: {simulation['observation']}"

    trace = ActionTrace(
        agent_id=action.agent_id,
        action_type=action.action_type,
        payload=action.payload,
        risk_score=score,
        risk_level=level,
        decision=decision,
        reason=final_reason
    )
    db.add(trace)
    db.commit()
    
    return RiskEvaluation(
        risk_score=score,
        risk_level=level,
        decision=decision,
        reason=final_reason,
        simulation_result=simulation
    )
    
    simulation = None
    # 2. Trigger Sandbox with Context Injection if risk is not LOW
    if level != "LOW":
        # We pass the context_files from the request into the sandbox
        simulation = run_in_sandbox(action.payload, action.context_files)
    
    # 3. Apply Policy
    decision = enforce_policy(level)
    
    # 4. Build the Final Reasoning (Brutalized for the Dashboard)
    final_reason = llm_decision.get("reason", "")
    
    if simulation:
        # Check if the simulation actually deleted our "Ghost Files"
        if "DELETED" in simulation.get("impact_report", ""):
            final_reason = f"🚨 CRITICAL IMPACT: {simulation['impact_report']} | {final_reason}"
        else:
            final_reason += f" | Sandbox Output: {simulation['observation']}"

    # 5. Log to DB
    trace = ActionTrace(
        agent_id=action.agent_id,
        action_type=action.action_type,
        payload=action.payload,
        risk_score=score,
        risk_level=level,
        decision=decision,
        reason=final_reason
    )
    db.add(trace)
    db.commit()
    
    return RiskEvaluation(
        risk_score=score,
        risk_level=level,
        decision=decision,
        reason=final_reason,
        simulation_result=simulation
    )

@router.get("/traces")
def get_traces(db: Session = Depends(get_db)):
    # Fetch latest 50 logs for the dashboard
    return db.query(ActionTrace).order_by(ActionTrace.timestamp.desc()).limit(50).all()