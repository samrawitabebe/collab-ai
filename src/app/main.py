from fastapi import FastAPI

from app.database.sqlalchemy import engine
from app.models.db import Base

from .api.v1.routes import router as v1_router

app = FastAPI(title="Collab AI", version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(v1_router, prefix="/v1")
