from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

services_category_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Где найти',
                callback_data='services_from_BU_',
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


def service_category_kb(service):
    service_category_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Где найти',
                    callback_data=f'services_from_BU_{service.id}',
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

    return service_category_kb
