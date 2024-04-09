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


user_crud = UserCRUD()
