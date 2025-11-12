from app.database.sqlalchemy import engine
from app.models.db import Base

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Database setup is working.")
