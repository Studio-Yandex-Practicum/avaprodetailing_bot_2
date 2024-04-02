from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)



reg_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Регистрация',
                #web_app=WebAppInfo(url='')
                
            ),
        ],
        
    ],
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
