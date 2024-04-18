from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import BusinessUnit


def build_business_units_keyboard(units: list[BusinessUnit]):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Создать новый бизнес-юнит',
            callback_data='create_business_unit'
        )
    )
    for unit in units:
        builder.row(
            InlineKeyboardButton(
                text=f'{unit.name}'
                     f' - {"Активен" if unit.is_active else "Неактивен"}',
                callback_data=f'business_unit_{unit.id}'
            )
        )
    return builder.as_markup()


business_unit_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Название',
                callback_data='edit_unit_name'
            ),
            InlineKeyboardButton(
                text='Описание',
                callback_data='edit_unit_note'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Адрес',
                callback_data='edit_unit_address'
            ),
            InlineKeyboardButton(
                text='Список услуг',
                callback_data='change_unit_status'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Вернуться в меню',
                callback_data='business_units'
            )
        ]
    ]
)


def business_unit_manage_keyboard(is_active: bool):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить данные',
                    callback_data='edit_unit'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Деактивировать' if is_active else 'Активировать',
                    callback_data='edit_unit_status'
                ),
            ]
        ]
    )
    return keyboard
