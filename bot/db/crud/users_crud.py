from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UsersCRUD:
    
    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: User,
    ):
        obj_in_data = obj_in.dict()
        db_obj = User(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(User).where(
                User.id == obj_id
            )
        )
        return db_obj.scalars().first()

users_crud = UsersCRUD()