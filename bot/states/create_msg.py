from aiogram.fsm.state import State, StatesGroup


class CreateMSG(StatesGroup):
    text = State()
    msg_id = State()
    unit_id = State()
