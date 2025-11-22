from fastapi import FastAPI

from app.api.routes import router
from app.api.v1.routes import router as executions_router
from app.database.models import Base
from app.database.sqlalchemy import engine


def create_app() -> FastAPI:
    app = FastAPI(
        title="Collab AI",
        description="Multi-agent SDLC orchestration system",
        version="0.1.0",
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(router)
    app.include_router(executions_router)

    return app


app = create_app()
