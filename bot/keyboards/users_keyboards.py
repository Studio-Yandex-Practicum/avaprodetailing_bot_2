from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup, WebAppInfo)

reg_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Регистрация',
                #web_app=WebAppInfo(url='')
                callback_data='Registration',
                
                
                
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
