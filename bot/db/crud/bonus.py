from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.base import CRUDBase
from bot.db.models import Bonus


class BonusCRUD(CRUDBase[Bonus]):
    async def add_multi(self, data: list[Bonus], session: AsyncSession):
        session.add_all(data)
        await session.commit()


bonuses_crud = BonusCRUD(Bonus)
