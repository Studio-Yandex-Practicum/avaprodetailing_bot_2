from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Bonus
from bot.db.crud.base import CRUDBase


class BonusCRUD(CRUDBase[Bonus]):
    async def add_multi(self, data: list[Bonus], session: AsyncSession):
        session.add_all(data)
        await session.commit()


bonuses_crud = BonusCRUD(Bonus)
