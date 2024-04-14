from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from bot.db.models.car import Car


identify_client_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отсканировать QR-код',
                callback_data='scan_qrcode'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Найти по номеру телефона',
                callback_data='find_by_phone'
            ),
        ],
    ]
)

find_phone_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Зарегистрировать',
                callback_data='register'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Ввести другой номер',
                callback_data='enter_another_number'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Вернуться к началу',
                callback_data='return_to_start'
            ),
        ],
    ]
)

client_profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Зарегистрировать посещение',
                callback_data='register_visit'
            ),
            InlineKeyboardButton(
                text='Баллы',
                callback_data='view_points'
            ),
            InlineKeyboardButton(
                text='Отчеты',
                callback_data='view_reports'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Редактировать профиль',
                callback_data='edit_profile'
            ),
        ],
    ]
)

def build_user_cars_keyboard(user_cars: list[Car]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for car in user_cars:
        button_text = f'{car.brand} {car.model} {car.number}'
        button_callback_data = f'car_selection_{car.id}'
        keyboard.add(InlineKeyboardButton(text=button_text,
                                          callback_data=button_callback_data))
    return keyboard

services_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить в чек',
                callback_data='add_to_receipt'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Следующая услуга',
                callback_data='next_service'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Завершить выбор',
                callback_data='finish_selection'
            ),
        ],
    ]
)

bonus_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Начислить баллы',
                callback_data='award_bonus'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Списать баллы',
                callback_data='use_bonus'
            ),
        ],
    ]
)

payment_acceptions_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Принять',
                callback_data='accept_payment'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отказать',
                callback_data='reject_payment'
            ),
        ],
    ]
)

ok_button = InlineKeyboardButton(text="ОК", callback_data="ok_button")
