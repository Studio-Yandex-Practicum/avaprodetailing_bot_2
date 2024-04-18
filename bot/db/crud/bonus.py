from bot.db.models import Bonus
from bot.db.crud.base import CRUDBase


bonuses_crud = CRUDBase[Bonus](Bonus)