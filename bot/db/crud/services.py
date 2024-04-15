from bot.db.crud.base import CRUDBase
from bot.db.models import Service, ServiceCategory

services_crud = CRUDBase[Service](Service)
category_crud = CRUDBase[ServiceCategory](ServiceCategory)
