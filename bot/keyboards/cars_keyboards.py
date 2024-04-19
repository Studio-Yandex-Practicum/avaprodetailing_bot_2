from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Изменить данные по автомобилям',
                callback_data='choose_car',
            )
        ],
        [
            InlineKeyboardButton(
                text='Добавить автомобиль',
                callback_data='add_car',
            )
        ],
        [
            InlineKeyboardButton(
                text='Вернуться в меню',
                callback_data='menu',
            )
        ],
    ],
)


add_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Внесите информацию об автомобиле',
                callback_data='add_car',
            )
        ],]
)


choose_car_kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text='Выберите автомобиль',
                callback_data='choose_car',
            )]
        ],
)


edit_car_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить марку',
                    callback_data='change_brand',
                )
            ],
            [
                InlineKeyboardButton(
                    text='Изменить модель',
                    callback_data='change_model',
                )
            ],
            [
                InlineKeyboardButton(
                    text='Изменить гос.номер',
                    callback_data='change_number',
                )
            ],
            [
                InlineKeyboardButton(
                    text='Удалить автомобиль из списка',
                    callback_data='delete_car',
                )
            ],
            [
                InlineKeyboardButton(
                    text='Вернуться к списку автомобилей',
                    callback_data='choose_car',
                )
            ]
        ],
)


verify_delete_car_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Удалить автомобиль из списка',
                callback_data='confirmed_delete',
            )
        ],
        [
            InlineKeyboardButton(
                text='Вернуться к списку автомобилей',
                callback_data='choose_car',
            )
        ],
    ],
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
                callback_data='menu',
            )
        ],
    ],
)