from sqlalchemy.orm import Session

from app.database import repositories
from app.database.sqlalchemy import SessionLocal
from app.models.base import ExecutionRequest
from app.models.db import RunStatus
from app.orchestrators.langgraph import LangGraphOrchestrator


async def execute_orchestration(
    run_id: str, orchestrator_name: str, payload: ExecutionRequest, db_session: Session
) -> None:
    run_repository = repositories.RUN

    with SessionLocal() as db_session:
        run = run_repository.get(db_session, run_id)
        if not run:
            return

        orchestrator = None
        if orchestrator_name.lower() == "langgraph":
            orchestrator = LangGraphOrchestrator()
        else:
            raise ValueError(f"Unsupported orchestrator: {orchestrator_name}")

        try:
            run = run_repository.get(db_session, run_id)
            if not run:
                return
            print(f"Starting execution for run_id: {run_id} with orchestrator: {orchestrator_name}")
            run.status = RunStatus.RUNNING
            db_session.commit()

            result = await orchestrator.execute(payload)
            run.status = RunStatus.COMPLETED if result.get("status") == "completed" else RunStatus.FAILED
            db_session.commit()
        except Exception:
            run = run_repository.get(db_session, run_id)
            if run:
                run.status = RunStatus.FAILED
                db_session.commit()
