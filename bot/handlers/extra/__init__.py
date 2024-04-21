from aiogram import Router

from . import business_units, car, super_admin, update_admin, report_mail

super_router = Router(name=__name__)
super_router.include_routers(
    super_admin.router, update_admin.router,
    business_units.router, car.router, report_mail.router
)
