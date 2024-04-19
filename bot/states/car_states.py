from aiogram.fsm.state import State, StatesGroup


class RegCar(StatesGroup):
    brand = State()
    model = State()
    number = State()
    user_id = State()


class ChooseCar(StatesGroup):
    chosen = State()
    new_brand = State()
    new_model = State()
    new_number = State()
