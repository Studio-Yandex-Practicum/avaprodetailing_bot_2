from bot.db.crud.base import CRUDBase
from bot.db.models import Car

cars_crud = CRUDBase[Car](Car)
