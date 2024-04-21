from bot.core.enums import UserRole
from bot.db.crud.base import CRUDBase
from bot.db.models import User
from typing import cast
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.enums import UserRole

class UserCRUD(CRUDBase[User]):
    async def get_multi_with_tg_user_id(self, session: AsyncSession):
        db_objs = await session.scalars(
            select(self.model).where(
                and_(User.role == UserRole.USER, User.tg_user_id != None) 
            )
        )
        return cast(User, db_objs.all())
    
users_crud = UserCRUD(User)
