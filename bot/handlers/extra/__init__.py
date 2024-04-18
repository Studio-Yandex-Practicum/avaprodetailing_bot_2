from aiogram import Router

from . import super_admin, car, business_units

super_router = Router(name=__name__)

super_router.include_routers(
    super_admin.router, business_units.router, car.router
)
