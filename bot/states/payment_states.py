from aiogram.fsm.state import StatesGroup, State


class PaymentProcess(StatesGroup):
    enter_payment = State()
    scan_qr_code = State()
