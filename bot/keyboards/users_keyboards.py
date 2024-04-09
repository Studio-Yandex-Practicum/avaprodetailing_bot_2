from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup, WebAppInfo)

reg_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Зарегестрироваться',
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

fsm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Регистрация',
            ),
        ],
    ],
)
