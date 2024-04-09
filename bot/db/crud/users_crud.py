from typing import Optional, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User


class UserCRUD:

    async def get(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[User]:
        return cast(
            Optional[User],
            await session.scalar(
                select(User).where(User.tg_user_id == user_id)
            ),
        )
    
    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> User:
        db_obj = await User.create_user_obj(obj_in=obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return cast(User, db_obj)


user_crud = UserCRUD()
