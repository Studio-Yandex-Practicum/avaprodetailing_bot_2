from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bonus_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Начислить баллы (+)",
                callback_data="add_bonus"
            ),
            InlineKeyboardButton(
                text="Списать баллы (-)",
                callback_data="spend_bonus"
            )
        ]
    ]
)

bonus_add_choice_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='5%',
                callback_data='bonus_add_5'
            ),
            InlineKeyboardButton(
                text='10%',
                callback_data='bonus_add_10'
            )
        ],
        [
            InlineKeyboardButton(
                text='Ввести %',
                callback_data='bonus_add_custom'
            ),
            InlineKeyboardButton(
                text='Ввести сумму',
                callback_data='bonus_add_sum'
            )
        ]
    ]
)

bonus_approve_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Подтвердить',
                callback_data='approve_bonus_add'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отменить',
                callback_data='cancel_bonus_add'
            )
        ]
    ]
)
