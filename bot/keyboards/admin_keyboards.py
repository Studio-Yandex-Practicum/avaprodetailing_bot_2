from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


super_admin_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Бизнес-юниты',
                callback_data='business_unit'
            ),
            InlineKeyboardButton(
                text='Каталог услуг',
                callback_data='service_catalog',
            )
        ],
        [
            InlineKeyboardButton(
                text='Администраторы',
                callback_data='administrators',
            ),
            InlineKeyboardButton(
                text='Клиенты',
                callback_data='clients'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отчеты',
                callback_data='reports',
            ),
            InlineKeyboardButton(
                text='Рассылки',
                callback_data='mailing',
            )
        ],
        [
            InlineKeyboardButton(
                text='Переключиться в режим администратора',
                callback_data='switch_admin_mode'
            ),
        ],
    ]
)

# Доработать, тесты
admin_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Найти клиента',
                callback_data='search_client'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Регистрация клиента',
                callback_data='reg_client'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отчеты',
                callback_data='admin_reports',
            ),
            InlineKeyboardButton(
                text='Инфо',
                callback_data='info',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Режим настройки',
                callback_data='extra_admin'
            ),
        ],
    ]
)