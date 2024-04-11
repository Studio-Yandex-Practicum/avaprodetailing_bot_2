from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.crud.users_crud import user_crud
from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE, STATE_FIO,
                                STATE_PHONE_NUMBER, THX_REG)
from bot.db.models.users import User
from bot.keyboards.users_keyboards import add_car_kb, agree_refuse_kb,back_menu_kb,profile_kb
from bot.states.user_states import RegUser
from bot.utils.validators import (validate_reg_birth_date, validate_reg_fio,
                                  validate_reg_phone_number)
from datetime import datetime

router = Router(name=__name__)