from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from core.database import Base

class ActionTrace(Base):
    __tablename__ = "action_traces"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    agent_id = Column(String, index=True)
    action_type = Column(String)
    payload = Column(String)
    risk_score = Column(Integer)
    risk_level = Column(String)
    decision = Column(String)
    reason = Column(String)