from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.bonus import Bonus, BonusCase
from bot.db.models.payment_transaction import Visit
from bot.db.models.users import User
from bot.keyboards.inline.payment_inline import (bonus_keyboard,
                                                 build_user_cars_keyboard,
                                                 client_profile_keyboard,
                                                 identify_client_keyboard,
                                                 ok_button,
                                                 payment_acceptions_keyboard,
                                                 reg_new_num,
                                                 services_keyboard)
from bot.utils.validators import check_user_exists_by_phone, get_user_cars, validate_phone_number

router = Router(name=__name__)


@router.callback_query(F.data == 'identify_client')
async def identify_client_callback(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer()
    await callback_query.message.bot.send_message(
        callback_query.from_user.id,
        'Выберите способ идентификации клиента',
        reply_markup=identify_client_keyboard
    )


@router.callback_query(F.data == 'find_by_phone')
async def find_by_phone_callback(callback_query: types.CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    await callback_query.answer()
    await callback_query.message.bot.send_message(
        callback_query.from_user.id,
        'Введите номер телефона в формате +78888888888:',
        reply_markup=types.ForceReply()
    )
    phone_number = callback_query.data
    if validate_phone_number(phone_number):
        if await check_user_exists_by_phone(phone_number, session):
            query = select(User).filter(User.phone_number == phone_number)
            result = await session.execute(query)
            user = result.scalar_one()
            profile_message = (
                f'Профиль клиента:\n'
                f'ФИО: {user.first_name} {user.last_name}\n'
                f'Дата рождения: {user.birth_date}\n'
                f'Номер телефона: {user.phone_number}\n'
                f'Баланс: {user.bonuses} бонусов'
            )
            await callback_query.message.bot.send_message(
                callback_query.from_user.id,
                profile_message,
                reply_markup=client_profile_keyboard
            )
        else:
            await callback_query.message.bot.send_message(
                callback_query.from_user.id,
                'Клиент с таким номером не зарегистрирован.',
                reply_markup=reg_new_num
            )
    else:
        await find_by_phone_callback(callback_query, session)


@router.callback_query(F.data == 'register_visit')
async def register_visit_callback(callback_query: types.CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    await callback_query.answer()
    user_id = callback_query.from_user.id
    user_cars = await get_user_cars(user_id, session)
    keyboard = build_user_cars_keyboard(user_cars)
    await callback_query.message.bot.send_message(
        user_id,
        'Выберите автомобиль клиента:',
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'select_services')
async def select_services_callback(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer()
    await callback_query.message.bot.send_message(
        callback_query.from_user.id,
        'Выберите оказанные услуги',
        reply_markup=services_keyboard
    )


@router.callback_query(F.data == 'service_selection')
async def service_selection_callback(callback_query: types.CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    await callback_query.answer()
    user_id = callback_query.from_user.id
    car_info = callback_query.data.get('car_info')
    selected_services = callback_query.data('service_id')
    visit_info = f'Посещение клиента:\n{car_info}\n{selected_services}\n\nВведите общую сумму посещения:'
    await callback_query.message.bot.send_message(
        user_id,
        visit_info,
        reply_markup=types.ForceReply()
    )


@router.message_handler(lambda message: message.text.isdigit(), state="*")
async def process_visit_summ(message: types.Message, state: FSMContext, session: AsyncSession):
    async with state.proxy() as data:
        data['visit_summ'] = message.text
    try:
        visit_summ = float(message.text)
        if visit_summ < 0:
            raise ValueError
    except ValueError:
        await message.reply('Введите корректную положительную сумму с дробной частью '
                            '(до двух знаков после запятой)')
        return
    await message.reply('Выберите услуги, оказанные клиенту:', reply_markup=services_keyboard)
    await Visit.service_id


@router.callback_query_handler(F.data == 'finish_selection', F.state == '*')
async def finish_selection_callback(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.answer()
    await callback_query.message.delete()
    async with state.proxy() as data:
        visit_summ = data['visit_summ']
    visit_data = await state.get_data()
    visit = Visit(
        user_id=visit_data['user_id'],
        car_id=visit_data['car_id'],
        service_id=visit_data['service_id'],
        summ=visit_summ,
    )
    session.add(visit)
    await session.commit()
    client_id = visit_data['user_id']
    client = await session.get(User, client_id)
    possible_bonus_usage = min(int(client.bonuses * 0.98), int(visit_summ))
    message_text = (
        f'Посещение клиента:\n'
        f'{visit_data["car_info"]}\n'
        f'{visit_data["selected_services"]}\n'
        f'{visit_summ} рублей\n\n'
        f'У клиента {client.bonuses} баллов. Может быть списано {possible_bonus_usage}.\n\n'
        f'(Сумма возможно списания: {possible_bonus_usage})'
    )
    await callback_query.message.reply(message_text, reply_markup=bonus_keyboard)
    await state.finish()


@router.callback_query(F.data == 'use_bonus')
async def use_bonus_callback(callback_query: types.CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    await callback_query.answer()
    user_id = callback_query.from_user.id
    bonus = await session.query(Bonus).filter(Bonus.user_id == user_id).one_or_none()
    if bonus is None:
        await callback_query.message.bot.send_message(
            user_id,
            'У вас нет бонусов.'
        )
        return
    bonus_case = await session.query(BonusCase).filter(BonusCase.id == bonus.case_id).one_or_none()
    if bonus_case is None:
        await callback_query.message.bot.send_message(
            user_id,
            'Не удалось получить информацию о кейсе бонусов.'
        )
        return
    message_text = (
        f'У клиента {bonus.full_amount} баллов. '
        f'Может быть списано {min(bonus.full_amount - bonus.used_amount, bonus_case.amount)}.\n\n'
        f'(Сумма возможно списания: {min(bonus.full_amount - bonus.used_amount, bonus_case.amount)})'
    )
    await callback_query.message.bot.send_message(
        user_id,
        message_text,
        reply_markup=types.ForceReply()
    )


@router.callback_query(F.data == 'accept_payment')
async def accept_payment_callback(callback_query: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.delete()
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        visit_data = data['visit_data']
        visit_summ = data['visit_summ']
        bonus_usage = data['bonus_usage']
    total_payment = visit_summ - bonus_usage
    message_text = (
        f'Посещение клиента:\n'
        f'{visit_data["car_info"]}\n'
        f'{visit_data["selected_services"]}\n'
        f'{visit_summ} рублей\n\n'
        f'Будет списано {bonus_usage} баллов\n\n'
        f'К оплате {total_payment} рублей\n\n'
    )
    await callback_query.message.bot.send_message(
        user_id,
        message_text,
        reply_markup=payment_acceptions_keyboard
    )


@router.callback_query(F.data == 'ok_button')
async def ok_button_callback(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer()
    await callback_query.message.bot.send_message(
        callback_query.from_user.id,
        "act = 0;",
        reply_markup=ok_button()
    )


@router.callback_query(F.data == 'reject_payment')
async def reject_payment_callback(callback_query: types.CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    await callback_query.answer()
    await use_bonus_callback(callback_query, session)
