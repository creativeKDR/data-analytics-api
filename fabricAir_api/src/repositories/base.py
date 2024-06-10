from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.storeFile import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.ID == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 5000) -> List[ModelType]:
        return db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        db.commit()
        return db_obj

    def update(self, db: Session, id: any, *, obj_in: Union[UpdateSchemaType]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = jsonable_encoder(obj_in)
        else:
            update_data = jsonable_encoder(obj_in)
        db_obj = db.query(self.model).filter(self.model.ID == id).update(update_data)
        db.commit()
        return db_obj

    def remove(self, db: Session, *, id: str, obj_in: Union[UpdateSchemaType]) -> ModelType:
        update_data = jsonable_encoder(obj_in)
        db_obj = db.query(self.model).filter(self.model.ID == id).update(update_data)
        db.commit()
        return db_obj
