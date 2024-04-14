from aiogram.fsm.state import State, StatesGroup


class RegCar(StatesGroup):
    brand = State()
    model = State()
    number = State()
