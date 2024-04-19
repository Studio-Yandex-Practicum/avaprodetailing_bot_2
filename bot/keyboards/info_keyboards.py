from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

info_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Бизнес-юниты и услуги',
                callback_data='info_business_unit',
            )
        ],
        [
            InlineKeyboardButton(
                text='Бонусная программа',
                callback_data='info_bonus_programm',
            )
        ],
    ],
)

info_bonus_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Ок',
                callback_data='info',
            )
        ],
    ],
)
