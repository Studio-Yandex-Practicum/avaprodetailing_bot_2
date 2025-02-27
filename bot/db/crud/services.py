from bot.db.crud.base import CRUDBase
from bot.db.models import Service
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Generic, Optional, Type, TypeVar, cast

from sqlalchemy import select

services_crud = CRUDBase[Service](Service)
