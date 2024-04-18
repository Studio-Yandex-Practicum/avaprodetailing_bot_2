from aiogram import Router

from . import super_admin, update_admin

super_router = Router(name=__name__)
super_router.include_routers(super_admin.router, update_admin.router)
