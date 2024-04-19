from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

reg_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Зарегистрироваться',
                #web_app=WebAppInfo(url='')
                callback_data='Registration',
            ),
        ],
    ],
)

agree_refuse_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Согласиться',
                callback_data='agree',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отказаться',
                callback_data='Registration',
            ),
        ],
    ]
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Профиль',
                callback_data='profile',
            ),
            InlineKeyboardButton(
                text='Каталог услуг',
                callback_data='service_catalog',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Автомобили',
                callback_data='car_menu',
            ),
            InlineKeyboardButton(
                text='История',
                callback_data='history',
            )
        ],
        [
            InlineKeyboardButton(
                text='Предъявить QR код',
                callback_data='generate_qr_code',
            )
        ],   
    ]
)

back_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Вернуться в меню',
                callback_data='menu',
            )
        ],
    ]
)

add_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить автомобиль',
                callback_data='car_menu',
            )
        ],
    ]
)



service_category_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить автомобиль',
                callback_data='add_car',
            ),
            InlineKeyboardButton(
                text='Добавить автомобиль',
                callback_data='add_car',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Сменить категорию',
                callback_data='service_catalog',
            )
        ],
    ]
)
