from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Найти клиента',
                callback_data='search_phone_number'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Регистрация клиента',
                callback_data='search_phone_number'
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

admin_back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Вернуться в меню',
                callback_data='admin_main_menu'
            )
        ]
    ]
)

admin_reg_client = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Зарегистрировать',
                callback_data='reg_client',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Ввести другой номер',
                callback_data='search_phone_number',
            )
        ],
    ]
)

reg_or_menu_adm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Зарегистрировать',
                callback_data='profile_before_search',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отменить',
                callback_data='admin_main_menu',
            ),
        ],
    ]
)

client_profile_for_adm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Зарегистрировать посещение',
                callback_data='reg_visit',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Баллы',
                callback_data='get_bonus',
            ),
            InlineKeyboardButton(
                text='Отчеты',
                callback_data='report_for_adm',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Редактировать профиль',
                callback_data='update_profile'
            ),
        ],
    ]
)

update_profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Изменить данные клиента',
                callback_data='update_client_data',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Изменить данные по автомобилям',
                callback_data='TODO',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Заблокировать клиента',
                callback_data='block_client',
            ),
        ]
    ]
)

update_client_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Изменить ФИО',
                callback_data='update_client_fio',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Изменить дату рождения',
                callback_data='update_client_birth_date',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Изменить номер телефона',
                callback_data='update_client_phone_number',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Комментарий',
                callback_data='update_client_note',
            ),
        ],
    ]
)

add_update_data = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='ОК',
                callback_data='OK_update_client',
            ),
        ],
    ]
)
#profile_before_search

adddd_data = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='ОК',
                callback_data='profile_before_search',
            ),
        ],
    ]
)