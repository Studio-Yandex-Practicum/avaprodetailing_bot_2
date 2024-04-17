from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

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
                callback_data='cars',
            ),
            InlineKeyboardButton(
                text='История',
                callback_data='Reports',
            )
        ],
        [
            InlineKeyboardButton(
                text='Предъявить QR код',
                callback_data='qr_code',
            )
        ],
        [
            InlineKeyboardButton(
                text='Баланс бонусов',
                callback_data='view_balance',
            )
        ]    
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
                callback_data='add_car',
            )
        ],
    ]
)

view_bonuses = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Баланс бонусов',
                callback_data='view_bonus',
            )
        ],
    ]
)


manage_bonus_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Начислить баллы (+)", callback_data="add_bonus"), 
        InlineKeyboardButton(text="Списать баллы (-)", callback_data="spend_bonus")
    ]
])