from bot.db.crud.base import CRUDBase
from bot.db.models import User

users_crud = CRUDBase[User](User)


