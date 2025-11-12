from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import repositories
from app.models.db import Base, RunStatus


def test_create_and_get_run():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    run_repo = repositories.RUN

    run_repo.create(
        db,
        {"id": "test123", "orchestrator": "langgraph", "status": RunStatus.PENDING},
    )

    fetched = run_repo.get(db, "test123")

    assert fetched is not None
    assert fetched.orchestrator == "langgraph"
    assert fetched.status == RunStatus.PENDING
