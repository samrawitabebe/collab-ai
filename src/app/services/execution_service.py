from app.api.models import ExecutionRequest
from app.database import repositories
from app.database.models import RunStatus
from app.database.sqlalchemy import SessionLocal
from app.orchestrators.utils import get_orchestrator


async def execute_orchestration(run_id: str, payload: ExecutionRequest) -> None:
    run_repository = repositories.RUN

    with SessionLocal() as db_session:
        run = run_repository.get(db_session, run_id)
        if not run:
            return

        orchestrator = get_orchestrator(payload.orchestrator)

        try:
            print(f"Starting execution for run_id: {run_id} with orchestrator: {payload.orchestrator}")
            run.status = RunStatus.RUNNING
            db_session.commit()

            result = await orchestrator.execute(payload)
            print(f"Execution completed for run_id: {run_id} with result: {result}")
            run.output_json = result
            run.status = RunStatus.COMPLETED
            db_session.commit()
        except Exception as e:
            print(f"Execution failed for run_id: {run_id} with error: {e}")
            run = run_repository.get(db_session, run_id)
            if run:
                run.status = RunStatus.FAILED
                db_session.commit()
