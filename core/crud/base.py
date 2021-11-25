from typing import TypeVar, List

from fastapi import HTTPException
from sqlmodel import SQLModel, Session, select
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=SQLModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase:

    model: ModelType

    def create(self, obj: SchemaType, session: Session) -> ModelType:
        to_object = self.model.from_orm(obj)
        session.add(to_object)
        session.commit()
        session.refresh(to_object)
        return to_object

    def list_create(self, objects: List[SchemaType], session: Session) -> dict:
        for o in objects:
            to_object = self.model.from_orm(o)
            session.add(to_object)
        session.commit()
        return {"ok": True}

    def get(self, session: Session, obj_id: int, ) -> ModelType:
        to_object = session.exec(select(self.model).filter_by(id=obj_id)).one()
        if not to_object:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} by id {obj_id} not found")
        return to_object

    def get_all(self, session: Session) -> List[ModelType]:
        to_objects = session.query(self.model).all()
        if not to_objects:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return to_objects

    def update(self, session: Session, obj_id: int, obj_update: SchemaType) -> ModelType:
        to_object = session.get(self.model, obj_id)
        if not obj_id:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} by id {obj_id} not found")
        obj_data = obj_update.dict(exclude_unset=True)
        for key, value in obj_data.values():
            setattr(to_object, key, value)

        session.add(to_object)
        session.commit()
        session.refresh(to_object)
        return to_object

    def delete(self, session: Session, obj_id: int) -> dict:
        to_obj = session.get(self.model, obj_id)
        if not obj_id:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} by id {obj_id} not found")
        session.delete(to_obj)
        session.commit()
        return {"ok": True}






