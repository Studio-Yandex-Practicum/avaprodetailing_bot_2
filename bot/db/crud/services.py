from bot.db.crud.base import CRUDBase
from bot.db.models import Service

services_crud = CRUDBase[Service](Service)