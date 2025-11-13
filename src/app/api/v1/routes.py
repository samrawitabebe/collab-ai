from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import repositories
from app.database.sqlalchemy import get_db
from app.models.base import ExecutionRequest, ExecutionResponse, ExecutionResult
from app.models.db import RunCreateInput, RunStatus
from app.services.execution_service import execute_orchestration

router = APIRouter()

run_repository = repositories.RUN


@router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/executions",
    tags=["executions"],
    response_model=ExecutionResponse,
    status_code=status.HTTP_200_OK,
)
async def create_execution(
    request: ExecutionRequest, background_tasks: BackgroundTasks, db_session: Annotated[Session, Depends(get_db)]
) -> ExecutionResponse:
    run_id = str(uuid4())
    run_repository.create(
        db_session, RunCreateInput(id=run_id, orchestrator=request.orchestrator, status=RunStatus.PENDING).model_dump()
    )

    background_tasks.add_task(execute_orchestration, run_id, request.orchestrator, request, db_session)

    return ExecutionResponse(run_id=run_id)


@router.get("/executions/{run_id}", tags=["executions"], response_model=ExecutionResult)
def get_execution(run_id: str, db_session: Annotated[Session, Depends(get_db)]) -> ExecutionResult:
    run = run_repository.get(db_session, run_id)
    print(run)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return ExecutionResult.model_validate(run)
