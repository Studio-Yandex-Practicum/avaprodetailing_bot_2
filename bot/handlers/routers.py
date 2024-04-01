from aiogram import Router

from .user import user_router
from states.users_states import router as user_state_router


main_router = Router(name='main_router')

main_router.include_routers(user_router)
main_router.include_router(user_state_router)
