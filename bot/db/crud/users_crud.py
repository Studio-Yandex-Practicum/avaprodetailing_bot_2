from datetime import datetime as dt
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
        obj_in_data = obj_in
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = User(
            phone_number=obj_in['phone_number'],
            last_name=obj_in['fio'].split(' ')[0],
            first_name=obj_in['fio'].split(' ')[1],
            middle_name=obj_in['fio'].split(' ')[2],
            birth_date=dt.strptime(obj_in['birth_date'], '%d.%m.%Y').date(),
            tg_user_id=obj_in['tg_user_id'],
        )  # получение данных из стейтов
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return cast(User, db_obj)


user_crud = UserCRUD()
