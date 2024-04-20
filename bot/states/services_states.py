from aiogram.fsm.state import State, StatesGroup


class AddServices(StatesGroup):
    name = State()
    description = State()


class AddCategory(StatesGroup):
    name = State()
    description = State()
    category_name = State()
