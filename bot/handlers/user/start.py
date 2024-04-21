from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.payload import decode_payload
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (CLIENT_BIO, PROFILE_MESSAGE_WITH_INLINE,
                                WELCOME_ADMIN_MESSAGE, WELCOME_REG_MESSAGE,
                                WELCOME_SUPER_ADMIN_MESSAGE)
from bot.core.enums import UserRole
from bot.db.crud.users import users_crud
from bot.keyboards.admin_keyboards import client_profile_for_adm
from bot.keyboards.super_admin_keyboards import (gener_admin_keyboard,
                                                 super_admin_main_menu)
from bot.keyboards.users_keyboards import profile_kb, reg_kb
from bot.utils.validators import check_user_is_admin, check_user_is_none

router = Router(name=__name__)


@router.message(CommandStart(deep_link=True))
async def decode_qr(
    message: Message, command: CommandObject,
    state: FSMContext, session: AsyncSession
):
    if await check_user_is_admin(
        tg_id=message.from_user.id, session=session
    ) and command.args is not None:
        await message.delete()
        payload = decode_payload(command.args)
        if not payload.isdigit():
            await message.answer('Произошла ошибка при сканировании.')
            return
        user = await users_crud.get_by_attribute(
            attr_name='tg_user_id', attr_value=int(payload), session=session
        )
        msg = await message.answer(
            CLIENT_BIO.format(
                last_name=user.last_name,
                first_name=user.first_name,
                birth_date=user.birth_date,
                phone_number=user.phone_number,
                balance=user.balance,
                note=user.note
            ),
            reply_markup=client_profile_for_adm
        )
        await state.update_data(
            phone_number=user.phone_number, msg_id=msg.message_id
        )


@router.message(CommandStart())
async def start(message: Message, session: AsyncSession, state: FSMContext):
    state_data = await state.get_data()
    tg_id = message.from_user.id
    await message.delete()
    db_obj = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=tg_id,
        session=session
    )
    if await check_user_is_none(tg_id=tg_id, session=session):
        await message.answer(
            WELCOME_REG_MESSAGE,
            reply_markup=reg_kb,
        )
        return
    if await check_user_is_admin(
        tg_id=tg_id, session=session
    ):
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
        )
