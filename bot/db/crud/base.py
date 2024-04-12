from typing import Any, Generic, Optional, Type, TypeVar, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.base import Base

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
        return cast(
            Optional[self.model],
            await session.scalars(
                select(self.model).where(self.model.id == obj_id)
            ).first(),
        )

    async def get_by_attribute(
        self,
        session: AsyncSession,
        attr_name: str,
        attr_value
    ) -> Optional[ModelType]:
        return cast(
            Optional[self.model],
            await session.scalars(
                select(self.model).where(
                    getattr(self.model, attr_name) == attr_value
                )
            ).first(),
        )

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        db_objs = await session.scalars(select(self.model))
        return cast(list[ModelType], db_objs.all())

    async def create(
        self,
        obj_in: dict[str, Any],
        session: AsyncSession,
    ):
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        await session.commit()
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in: dict[str, Any],
        session: AsyncSession,
    ):
        obj_data = db_obj.__dict__.items()

        for field, value in obj_data:
            if field in obj_in:
                setattr(db_obj, field, value)
        session.add(db_obj)
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
