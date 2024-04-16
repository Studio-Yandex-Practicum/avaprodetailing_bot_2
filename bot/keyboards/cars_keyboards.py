from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)


car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить автомобиль',
                callback_data='add_car',
            )
        ],
        [
            InlineKeyboardButton(
                text='Посмотреть автомобили',
                callback_data='view_car',
            )
        ]
    ],
)
