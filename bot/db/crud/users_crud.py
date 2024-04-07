from datetime import datetime as dt
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User


class UserCRUD:

        
    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(User).where(
                User.tg_user_id == obj_id
            )
        )
        return db_obj.scalars().first()
    
    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        obj_in_data = obj_in
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = User(
            phone_number = obj_in['phone_number'],
            last_name = obj_in['fio'].split(' ')[0],
            first_name = obj_in['fio'].split(' ')[1],
            middle_name = obj_in['fio'].split(' ')[2],
            birth_date = dt.strptime(obj_in['birth_date'],'%d.%m.%Y').date(),
            tg_user_id = obj_in['tg_user_id'],
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    
user_crud = UserCRUD()


#
            