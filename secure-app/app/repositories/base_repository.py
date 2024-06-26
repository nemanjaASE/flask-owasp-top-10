from typing import Type, TypeVar, Generic, List, Optional
from app.db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.repositories.exceptions import NotFoundError, DatabaseError 

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]) -> None:
        self.model = model

    def get_by_id(self, id: str) -> Optional[T]:
        try:
            instance = self.model.query.get(id)
            if instance is None:
                raise NotFoundError(self.model.__name__, id)
            return instance
        except SQLAlchemyError as e:
            raise DatabaseError(e)

    def get_all(self) -> List[T]:
        try:
            return self.model.query.all()
        except SQLAlchemyError as e:
            raise DatabaseError(e)

    def create(self, instance: T) -> T:
        try:
            db.session.add(instance)
            db.session.commit()
            return instance
        except IntegrityError as e:
            db.session.rollback()
            raise DatabaseError(e)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(e)

    def update(self, id: str, **kwargs) -> T:
        try:
            instance = self.get_by_id(id)
            if instance is None:
                raise NotFoundError(self.model.__name__, id)
            for key, value in kwargs.items():
                setattr(instance, key, value)
            db.session.commit()
            return instance
        except IntegrityError as e:
            db.session.rollback()
            raise DatabaseError(e)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(e)

    def delete(self, id: str) -> T:
        try:
            instance = self.get_by_id(id)
            if instance is None:
                raise NotFoundError(self.model.__name__, id)
            db.session.delete(instance)
            db.session.commit()
            return instance
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(e)