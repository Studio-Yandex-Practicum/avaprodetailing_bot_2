from bot.db.crud.base import CRUDBase
from bot.db.models.payment_transaction import Visit

visit_crud = CRUDBase[Visit](Visit)
