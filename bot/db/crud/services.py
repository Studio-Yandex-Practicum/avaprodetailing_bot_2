from bot.db.crud.base import CRUDBase
from bot.db.models import Service
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Generic, Optional, Type, TypeVar, cast
from sqlalchemy import select

class ServiceCRUD(CRUDBase[Service]):

    async def get_multi_by_attr(
        self,
        session: AsyncSession,
        attr_name: str,
        attr_value
    ):
        db_obj = await session.scalars(
            select(self.model).where(
                getattr(self.model, attr_name) == attr_value
            )
        )
        return cast(self.model, db_obj)



services_crud = ServiceCRUD(Service)