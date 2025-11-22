from typing import Any
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database.models import Execution, ExecutionStatus


class ExecutionRepository:
    """
    Repository wrapper for the Execution table.
    Handles creation, retrieval, and updates.
    """

    def create(
        self,
        db_session: Session,
        requirement: str,
        orchestrator: str,
        status: ExecutionStatus = ExecutionStatus.PENDING,
    ) -> Execution:
        execution = Execution(
            id=str(uuid4()),
            requirement=requirement,
            orchestrator=orchestrator,
            status=status,
        )
        db_session.add(execution)
        db_session.commit()
        db_session.refresh(execution)
        return execution

    def get(self, db_session: Session, execution_id: str) -> Execution | None:
        return db_session.query(Execution).filter(Execution.id == execution_id).first()

    def update(
        self,
        db_session: Session,
        execution: Execution,
        *,
        status: ExecutionStatus | None = None,
        result: dict[str, Any] | None = None,
    ) -> Execution:
        if status is not None:
            execution.status = status
        if result is not None:
            execution.result = result

        db_session.commit()
        db_session.refresh(execution)
        return execution


execution_repository = ExecutionRepository()
