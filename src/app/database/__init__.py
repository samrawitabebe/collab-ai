from app.database.models import Run
from app.database.repository import Repository


class Repositories:
    RUN = Repository(Run)


repositories = Repositories()
