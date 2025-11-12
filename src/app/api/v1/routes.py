from uuid import uuid4

from fastapi import APIRouter, status

from app.api.models.base import ExecutionRequest, ExecutionResponse

router = APIRouter()


@router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/executions",
    tags=["executions"],
    response_model=ExecutionResponse,
    status_code=status.HTTP_200_OK,
)
async def create_execution(request: ExecutionRequest) -> ExecutionResponse:
    run_id = str(uuid4())
    return ExecutionResponse(run_id=run_id)
