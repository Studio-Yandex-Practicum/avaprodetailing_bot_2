from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import WELCOME_SUPER_ADMIN_MESSAGE
from bot.core.enums import UserRole
from bot.db.crud.business_units import business_units_crud
from bot.db.crud.users import users_crud
#from bot.keyboards.business_units_keyboards import (
#    build_business_units_keyboard, report_business_units_keyboard,
#    select_type_report)
from bot.keyboards.super_admin_keyboards import (admin_bio_for_super_admin_kb,
                                                 gener_list_admins,
                                                 send_mailing_kb,
                                                 super_admin_back_kb,
                                                 super_admin_main_menu)
from bot.states.create_msg import CreateMSG
from bot.states.user_states import AdminState
#from bot.utils.create_pdf_report import pdf_report
from bot.db.crud.visit_crud import visit_crud

router = Router(name=__name__)



@router.callback_query(F.data == 'mailing')
async def create_mail(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    await callback.message.delete()
    await state.set_state(CreateMSG.text)
    msg = await callback.message.answer(
        text='Введите текст рассылки для клиентов',
    )
    await state.update_data(msg_id=msg.message_id)


@router.message(CreateMSG.text)
async def update_state_mail(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    
    await state.update_data(text=msg.text)
    await msg.delete()
    state_data = await state.get_data()
    await msg.bot.edit_message_text(
        text=(
            'Подтвердите корректность текста для отправки'
            f'\n\n{state_data.get("text")}'
        ),
        chat_id=msg.from_user.id,
        message_id=state_data.get('msg_id'),
        reply_markup=send_mailing_kb
    )


@router.callback_query(F.data == 'send_mailing')
async def send_mailing(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    users = await users_crud.get_multi_with_tg_user_id(
        session=session
    )
    print(users)
    
    for user in users:
        await msg.bot.send_message(
            chat_id=user.tg_user_id,
            text=state_data.get('text')
        )
    await msg.bot.edit_message_text(
        text='Рассылка отправлена',
        chat_id=msg.from_user.id,
        message_id=state_data.get('msg_id'),
        reply_markup=super_admin_back_kb,
    )
