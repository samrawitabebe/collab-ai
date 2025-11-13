from app.database.models import Base
from app.database.sqlalchemy import engine

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Database setup is working.")
