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
                callback_data='report_client_for_admin',
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
                callback_data='update_car_data',
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






finish_add_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить ещё один автомобиль',
                callback_data='add_car',
            )
        ],
        [
            InlineKeyboardButton(
                text='Вернуться в меню',
                callback_data='update_car_data',
            )
        ],
    ],
)


admin_edit_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Изменить марку',
                callback_data='admin_change_brand',
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить модель',
                callback_data='admin_change_model',
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить гос.номер',
                callback_data='admin_change_number',
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить тип кузова',
                callback_data='admin_edit_bodytype',
            )
        ],
        [
            InlineKeyboardButton(
                text='Удалить автомобиль из списка',
                callback_data='admin_delete_car',
            )
        ],
        [
            InlineKeyboardButton(
                text='Вернуться к списку автомобилей',
                callback_data='update_car_data',
            )
        ]
    ],
)


admin_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Вернуться в меню',
                callback_data='update_car_data',
            )
        ],
    ],
)


admin_verify_delete_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Удалить автомобиль из списка',
                callback_data='admin_confirmed_delete',
            )
        ],
        [
            InlineKeyboardButton(
                text='Вернуться к списку автомобилей',
                callback_data='update_car_data',
            )
        ],
    ],
)
