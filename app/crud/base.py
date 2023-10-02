from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.db.base import ORMBase

ModelType = TypeVar("ModelType", bound=ORMBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | None:
        return (
            db.execute(select(self.model).where(and_(self.model.id == id)))
            .scalars()
            .first()
        )

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        limit = min(500, limit)  # don't allow for arbitrarily large queries
        return db.execute(select(self.model)).scalars().all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:  # noqa
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
            else:
                raise AttributeError(
                    f"{self.model.__name__} does't have field '{field}'"
                )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.get(self.model, id)
        db.delete(obj)
        db.commit()
        return obj


class CRUDBaseWithOwner(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        super().__init__(model)

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        return db.scalar(
            select(func.count())
            .select_from(self.model)
            .filter(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )

    def create_with_owner(
        self, db: Session, *, obj_in: CreateSchemaType, owner_id: int
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
