from aiogram.types import (
    ReplyKeyboardMarkup, # крепится под полем ввода
    KeyboardButton, # Кнопки для верхней клавиатуры
    InlineKeyboardMarkup, # Крепится под сообщениями
    InlineKeyboardButton,
    WebAppInfo
)



reg_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Регистрация',
                web_app=WebAppInfo(url='https://vc.ru/u/2092914-codecash/775509-urok-11-veb-prilozhenie-v-telegram-bote')
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
