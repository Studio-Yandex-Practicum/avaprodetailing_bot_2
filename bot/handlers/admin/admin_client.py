from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE, STATE_FIO,
                                STATE_PHONE_NUMBER, THX_REG)
from bot.db.models.users import User
from bot.keyboards.users_keyboards import add_car_kb, agree_refuse_kb,back_menu_kb,profile_kb
from bot.states.user_states import RegUser
from datetime import datetime

router = Router(name=__name__)
