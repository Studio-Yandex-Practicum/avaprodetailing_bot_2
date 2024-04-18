from aiogram import Router

from . import super_admin
from . import car

super_router = Router(name=__name__)
super_router.include_routers(super_admin.router, car.router)
