from bot.db.crud.base import CRUDBase
from bot.db.models import ServiceCategory

category_crud = CRUDBase[ServiceCategory](ServiceCategory)