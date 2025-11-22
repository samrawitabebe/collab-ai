from enum import Enum

from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Execution(Base):
    """
    Represents a single orchestration execution.
    Stores all metadata plus the orchestrator's output JSON.
    """

    __tablename__ = "executions"

    id = Column(String, primary_key=True, index=True)
    requirement = Column(String, nullable=False)
    orchestrator = Column(String, nullable=False)

    status = Column(SAEnum(ExecutionStatus), nullable=False, default=ExecutionStatus.PENDING)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    result = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Execution id={self.id} status={self.status}>"
