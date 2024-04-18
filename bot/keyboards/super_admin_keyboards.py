from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


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