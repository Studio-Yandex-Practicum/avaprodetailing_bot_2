from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import Service
from bot.db.models.car import Car


def build_user_cars_keyboard(user_cars: list[Car]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for car in user_cars:
        button_text = f'{car.brand} {car.number}'
        button_callback_data = f'car_selection_{car.id}'
        keyboard.row(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data
            )
        )
    return keyboard.as_markup()


def build_services_keyboard(
    services: list[Service],
    chosen_services: list[int] = None
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for service in services:
        if service.id in chosen_services:
            button_text = '✅ ' + service.name
        else:
            button_text = service.name
        button_callback_data = f'service_id_{service.id}'
        keyboard.add(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text='Завершить выбор',
            callback_data='finish_selection'
        )
    )
    return keyboard.adjust(3).as_markup()


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

reg_new_num = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Зарегистрировать',
                callback_data='register_new_client'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Ввести другой номер',
                callback_data='enter_another_number'
            ),
        ],
    ]
)
