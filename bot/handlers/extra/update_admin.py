from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE,
                                STATE_FIO, STATE_PHONE_NUMBER, THX_REG,
                                WELCOME_ADMIN_MESSAGE, CLIENT_BIO,REF_CLIENT_INFO, WELCOME_SUPER_ADMIN_MESSAGE)
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.admin_keyboards import (admin_main_menu, admin_reg_client,
                                           client_profile_for_adm,
                                           reg_or_menu_adm,
                                           update_client_kb)
from bot.keyboards.super_admin_keyboards import gener_admin_keyboard, super_admin_main_menu
from bot.keyboards.users_keyboards import (add_car_kb, agree_refuse_kb,
                                           back_menu_kb, profile_kb)
from bot.states.user_states import AdminState, RegUser, SuperAdminState
from bot.utils.validators import validate_phone_number

router = Router(name=__name__)