from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UsersCRUD:
    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: User = None,
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = User(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

users_crud = UsersCRUD()