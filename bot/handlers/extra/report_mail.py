from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import WELCOME_SUPER_ADMIN_MESSAGE
from bot.core.enums import UserRole
from bot.db.crud.business_units import business_units_crud
from bot.db.crud.users import users_crud
from bot.keyboards.business_units_keyboards import (
    build_business_units_keyboard, report_business_units_keyboard,
    select_type_report)
from bot.keyboards.super_admin_keyboards import (admin_bio_for_super_admin_kb,
                                                 gener_list_admins,
                                                 send_mailing_kb,
                                                 super_admin_back_kb,
                                                 super_admin_main_menu)
from bot.states.create_msg import CreateMSG
from bot.states.user_states import AdminState
from bot.utils.create_pdf_report import pdf_report, report_info_client_for_admin
from bot.db.crud.payment_crud import visit_crud

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
    users = await users_crud.get_multi(session=session)
    
    for user in users:
        if user.role is UserRole.USER and user.tg_user_id is not None:
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


@router.callback_query(F.data == 'reports')
async def create_report(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    units = await business_units_crud.get_multi(session=session)
    await callback.message.delete()
    if units is None:
        msg = await callback.message.answer(
            text='Внесите информацию о Бизнес-юнитах',
            reply_markup=build_business_units_keyboard(units)
        )
        return
    msg = await callback.message.answer(
        'Выберите Бизнес-юнит',
        reply_markup=report_business_units_keyboard(units=units)
    )
    await state.update_data(msg_id=msg.message_id)
    

@router.callback_query(F.data.startswith('report_bis_unit_'))
async def selects_type_report(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    unit = await business_units_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    await state.update_data(unit_id=unit.id)
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text='Выберите отчет',
        chat_id=callback.from_user.id,
        message_id=state_data.get('msg_id'),
        reply_markup=select_type_report
    )
    

# FIXME
@router.callback_query(F.data == 'clients_unit')
async def create_report(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    
    
    users = await users_crud.get_multi(session=session)
    visits = await visit_crud.get_multi(session=session)
    state_data = await state.get_data()
    pdf_report(users=users,visits=visits)
    document = FSInputFile(path='report.pdf')
    await callback.bot.send_document(
        chat_id=callback.from_user.id,
        document=document,
        caption='Ваш отчет'
    )
    
# FIXME
@router.callback_query(F.data == 'visits_unit_report')
async def create_report(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    
    
    users = await users_crud.get_multi(session=session)
    visits = await visit_crud.get_multi(session=session)
    state_data = await state.get_data()
    pdf_report(users=users,visits=visits)
    document = FSInputFile(path='report.pdf')
    await callback.bot.send_document(
        chat_id=callback.from_user.id,
        document=document,
        caption='Ваш отчет'
    )



@router.callback_query(F.data == 'report_for_adm')
async def create_report(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        session=session,
        attr_name='phone_number',
        attr_value=state_data['phone_number']
    )

    
    report_info_client_for_admin(user=user)
    document = FSInputFile(path='report.pdf')
    await callback.bot.send_document(
        chat_id=callback.from_user.id,
        document=document,
        caption='Ваш отчет'
    )