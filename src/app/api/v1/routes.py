from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.api.models import ExecutionRequest, ExecutionResponse, ExecutionResult
from app.database.models import ExecutionStatus
from app.database.repository import execution_repository
from app.database.sqlalchemy import SessionLocal
from app.services.execution_service import execute_orchestration

router = APIRouter(prefix="/v1/executions", tags=["executions"])


@router.post("", response_model=ExecutionResponse)
async def create_execution(payload: ExecutionRequest, background_tasks: BackgroundTasks):
    """Create a new execution record and schedule its orchestration.

    Creates a Execution in the database with status PENDING, enqueues execute_orchestration
    as a background task, and returns a summary response.

    Args:
        payload (ExecutionRequest): Data describing the execution to create.
        background_tasks (BackgroundTasks): FastAPI BackgroundTasks for scheduling work.

    Returns:
        ExecutionResponse: Summary of the created execution (id, status, orchestrator, created_at).

    Side effects:
        Persists a Execution to the database and schedules execute_orchestration to run asynchronously.
    """

    with SessionLocal() as db_session:
        execution = execution_repository.create(
            db_session=db_session,
            requirement=payload.requirement,
            orchestrator=payload.orchestrator,
            status=ExecutionStatus.PENDING,
        )

        background_tasks.add_task(execute_orchestration, execution.id, payload)

        return ExecutionResponse(
            id=execution.id,
            status=execution.status,
            orchestrator=execution.orchestrator,
            created_at=execution.created_at,
        )


@router.get("/{execution_id}", response_model=ExecutionResult)
async def get_execution(execution_id: str):
    """
    Retrieve the execution details for a specific execution ID.

    Args:
        execution_id (str): The ID of the execution to retrieve.

    Returns:
        ExecutionResult: The details of the execution.

    Raises:
        HTTPException: If the execution is not found, a 404 error is raised.
    """
    with SessionLocal() as db_session:
        execution = execution_repository.get(db_session, execution_id)

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        return ExecutionResult(
            id=execution.id,
            orchestrator=execution.orchestrator,
            status=execution.status,
            created_at=execution.created_at,
            updated_at=execution.updated_at,
            result=execution.result,
        )
