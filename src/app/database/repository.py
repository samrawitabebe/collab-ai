from typing import Any, Generic, Optional, Type, TypeVar, cast

from sqlalchemy.orm import Session

from app.database.models import Base

T = TypeVar("T", bound=Base)


class Repository(Generic[T]):
    def __init__(self, model: Type[T]) -> None:
        self.model = model

    def create(self, db: Session, input: dict[str, Any]) -> T:
        instance: T = self.model(**input)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def get(self, db: Session, input: str) -> Optional[T]:
        return cast(Optional[T], db.get(self.model, input))

    def list(self, db: Session, limit: int = 100) -> list[T]:
        return db.query(self.model).limit(limit).all()
