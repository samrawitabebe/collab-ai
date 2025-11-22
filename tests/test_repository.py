from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base, Execution, ExecutionStatus
from app.database.repository import execution_repository


def test_create_and_get_execution():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    created = execution_repository.create(
        db_session=db,
        requirement="test requirement",
        orchestrator="langgraph",
        status=ExecutionStatus.PENDING,
    )

    fetched = execution_repository.get(db, created.id)

    assert fetched is not None
    assert isinstance(fetched, Execution)
    assert fetched.requirement == "test requirement"
    assert fetched.orchestrator == "langgraph"
    assert fetched.status == ExecutionStatus.PENDING
    assert fetched.result is None
