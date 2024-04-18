from bot.db.crud.base import CRUDBase
from bot.db.models import BusinessUnit

business_units_crud = CRUDBase[BusinessUnit](BusinessUnit)
