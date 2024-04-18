from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.handlers.user.registration import error_message
from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE,
                                STATE_FIO, STATE_PHONE_NUMBER, THX_REG,
                                WELCOME_ADMIN_MESSAGE, CLIENT_BIO,REF_CLIENT_INFO)
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.admin_keyboards import (admin_main_menu, admin_reg_client,
                                           client_profile_for_adm,
                                           reg_or_menu_adm,
                                           update_client_kb)
from bot.keyboards.users_keyboards import (add_car_kb, agree_refuse_kb,
                                           back_menu_kb, profile_kb)
from bot.states.user_states import AdminState, RegUser, SuperAdminState
from bot.utils.validators import validate_phone_number

router = Router(name=__name__)


@router.callback_query(F.data == 'switch_admin_mode')
async def admin_menu(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    tg_id = callback.from_user.id
    await state.clear()
    db_obj = await users_crud.get_by_attribute(
        attr_name='tg_user_id', attr_value=tg_id, session=session
    )
    await callback.message.delete()
    if db_obj.is_active:
        await callback.message.answer(
            WELCOME_ADMIN_MESSAGE,
            reply_markup=admin_main_menu
        )