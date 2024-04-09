from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оплатить наличными",
                callback_data="create_cash_payment",
            )
        ],
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="cancel_payment",
            )
        ]
    ]
)
