from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.core.enums import UserRole


super_admin_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Бизнес-юниты',
                callback_data='business_units'
            ),
            InlineKeyboardButton(
                text='Каталог услуг',
                callback_data='service_catalog',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Администраторы',
                callback_data='administrators',
            ),
            InlineKeyboardButton(
                text='Клиенты',
                callback_data='clients'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отчеты',
                callback_data='reports',
            ),
            InlineKeyboardButton(
                text='Рассылки',
                callback_data='mailing',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Режим администратора',
                callback_data='switch_admin_mode'
            ),
        ],
    ]
)


def gener_admin_keyboard(data):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Найти клиента',
            callback_data='search_phone_number'
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text='Регистрация клиента',
            callback_data='search_phone_number'
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text='Отчеты',
            callback_data='admin_reports',
        ),
        InlineKeyboardButton(
            text='Инфо',
            callback_data='info',
        ),
    )
            
    if data is UserRole.SUPERADMIN:
        builder.row(
            InlineKeyboardButton(
                text='Режим настройки',
                callback_data='extra_admin'
            ),
        )

    return builder.as_markup()


def gener_list_admins(data):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Зарегистрировать администратора',
            callback_data='reg_new_admin'
        ),
    )


    return builder.as_markup()