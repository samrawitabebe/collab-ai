from app.api.models import ExecutionRequest
from app.database.models import ExecutionStatus
from app.database.repository import execution_repository
from app.database.sqlalchemy import SessionLocal
from app.orchestrators.models import OrchestratorInput, OrchestratorResult
from app.orchestrators.utils import get_orchestrator


async def execute_orchestration(execution_id: str, payload: ExecutionRequest) -> None:
    """
    Run an orchestration in the background for a given execution ID and request.
    It is responsible for executing flow with the chosen orchestrator.
    """

    with SessionLocal() as db_session:
        execution = execution_repository.get(db_session, execution_id)
        if not execution:
            return

        orchestrator = get_orchestrator(payload.orchestrator)

        try:
            execution.status = ExecutionStatus.RUNNING
            db_session.commit()

            orchestrator_input = OrchestratorInput(
                requirement=payload.requirement,
                orchestrator=payload.orchestrator,
                human_approval_after=payload.human_approval_after,
            )

            result: OrchestratorResult = await orchestrator.execute(orchestrator_input)

            execution.result = result.model_dump()
            execution.status = ExecutionStatus.COMPLETED
            db_session.commit()

        except Exception as e:
            print(f"[ERROR] Orchestration failed for execution_id {execution_id}: {e}")
            execution = execution_repository.get(db_session, execution_id)
            if execution:
                execution.status = ExecutionStatus.FAILED
                db_session.commit()
