from app.database.repository import Repository
from app.models.db import Run


class Repositories:
    RUN = Repository(Run)


repositories = Repositories()
