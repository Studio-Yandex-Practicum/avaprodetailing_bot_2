from aiogram.fsm.state import State, StatesGroup


class RegUser(StatesGroup):
    fio = State()
    birth_date = State()
    phone_number = State()
    msg_id = State()
