from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base, ExecutionStatus
from app.database.repository import execution_repository


def test_create_and_get_execution():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    execution_repository.create(
        db,
        {"id": "test123", "orchestrator": "langgraph", "status": ExecutionStatus.PENDING},
    )

    fetched = execution_repository.get(db, "test123")

    assert fetched is not None
    assert fetched.orchestrator == "langgraph"
    assert fetched.status == ExecutionStatus.PENDING
