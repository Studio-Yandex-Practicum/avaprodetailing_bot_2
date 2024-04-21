from aiogram.fsm.state import StatesGroup, State


class CreateMSG(StatesGroup):
    text = State()
    msg_id = State()
    unit_id = State()