from bot.db.models import Bonus, User
from bot.db.crud.base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession


class BonusCRUD(CRUDBase[Bonus]):
    async def get_balance(user: User, session: AsyncSession):
        result = await session.scalar(select(func.sum(user.bonuses)).group_by(user.bonuses))