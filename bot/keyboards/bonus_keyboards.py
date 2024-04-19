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

spend_approve_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Подтвердить',
                callback_data='approve_spend_bonus'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отменить',
                callback_data='cancel_spend_bonus'
            )
        ]
    ]
)

spend_approve_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Подтвердить',
                callback_data='approve_spend_bonus'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отменить',
                callback_data='cancel_spend_bonus'
            )
        ]
    ]
)


def bonus_approve_amount_keyboard(callback_data):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Подтвердить',
                    callback_data=callback_data
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Отменить',
                    callback_data='admin_main_menu'
                )
            ]
        ]
    )
