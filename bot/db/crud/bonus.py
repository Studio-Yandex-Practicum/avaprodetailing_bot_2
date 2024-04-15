from bot.db.models.bonus import Bonus
from bot.db.crud.base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession


class BonusCRUD(CRUDBase[Bonus]):
    def __init__(self):
        super().__init__(Bonus)
