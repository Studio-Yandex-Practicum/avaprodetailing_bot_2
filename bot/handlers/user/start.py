from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE,
                                WELCOME_ADMIN_MESSAGE, WELCOME_MESSAGE,
                                WELCOME_REG_MESSAGE)
from bot.core.test_base import test_base
from bot.db.crud.users import users_crud
from bot.keyboards.admin_keyboards import (
    admin_main_menu,
    client_profile_for_adm,
)
from bot.keyboards.super_admin_keyboards import gener_admin_keyboard, super_admin_main_menu
from bot.keyboards.users_keyboards import profile_kb, reg_kb
from bot.utils.validators import check_user_is_admin, check_user_is_none

router = Router(name=__name__)


@router.message(CommandStart())
async def test(message: Message, session: AsyncSession, state: FSMContext):
    state_data = await state.get_data()
    tg_id = message.from_user.id
    # FIXME
    # await test_base(session=session)
    await message.delete()

    if await check_user_is_none(tg_id=tg_id, session=session):
        await message.answer(
            WELCOME_REG_MESSAGE,
            reply_markup=reg_kb,
        )
        return
    if await check_user_is_admin(tg_id=tg_id, session=session): # Закинул проверку актиности
        if db_obj.role is UserRole.ADMIN:
            await message.answer(
                WELCOME_ADMIN_MESSAGE,
                reply_markup=gener_admin_keyboard(data=db_obj.role),
            )
            return
        elif db_obj.role is UserRole.SUPERADMIN:
            if 'is_admin_menu' not in state_data:
                await message.answer(
                    WELCOME_SUPER_ADMIN_MESSAGE,
                    reply_markup=super_admin_main_menu
                )
                return
            await message.answer(
                WELCOME_ADMIN_MESSAGE,
                reply_markup=gener_admin_keyboard(data=db_obj.role),
            )
            return
    if db_obj.is_active:
        await message.answer(
            PROFILE_MESSAGE_WITH_INLINE,
            reply_markup=profile_kb
        ) # Пользователь зареган
