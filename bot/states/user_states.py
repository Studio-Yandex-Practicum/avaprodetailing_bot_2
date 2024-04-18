from aiogram.fsm.state import State, StatesGroup


class RegUser(StatesGroup):
    fio = State()
    birth_date = State()
    phone_number = State()
    msg_id = State()


class AdminState(StatesGroup):
    phone_number = State()
    phone_num_update = State()
    fio = State()
    birth_date = State()
    msg_id = State()
    user_id = State()
    note = State()
    is_active = State()
    reason_block = State()
    approv_block = State()
    payment_amount = State()


class SuperAdminState(StatesGroup):
    is_admin_menu = State()


class BusinessUnitState(StatesGroup):
    name = State()
    note = State()
    address = State()
    msg_id = State()
    unit_id = State()
    edit_field = State()
