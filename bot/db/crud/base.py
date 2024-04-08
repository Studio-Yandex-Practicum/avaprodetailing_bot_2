from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.db.models.base import Base
from bot.db.models.user import User

ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(Generic[ModelType]):

    def __init__(
            self,
            model: Type[ModelType]
    ):
        self.model = model

    async def get(
            self,
            session: AsyncSession,
            obj_id: int,
    ) -> Optional[ModelType]:
        db_obj = await session.scalars(
            select(self.model).where(
                self.model.id == obj_id
            )).first()
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        db_objs = await session.scalars(select(self.model)).all()
        return db_objs

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        await session.merge(db_obj)
        await session.commit()
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = db_obj.__dict__.items()
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field[0] in update_data:
                setattr(db_obj, field[0], field[1])
        await session.merge(db_obj)
        await session.commit()
        return db_obj

    async def remove(
            self,
            session: AsyncSession,
            db_obj: ModelType,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
