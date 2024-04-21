from bot.db.crud.base import CRUDBase
from bot.db.models.visit import Visit

visit_crud = CRUDBase[Visit](Visit)
