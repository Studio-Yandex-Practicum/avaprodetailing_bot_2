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
    bonus_method = State()
    bonus_to_add = State()
    bonus_to_spend = State()
    full_amount = State()
    brand = State()
    model = State()
    number = State()
    bodytype = State()
    brand_update = State()
    model_update = State()
    number_update = State()
    new_bodytype = State()
    chosen_car = State()


class SuperAdminState(StatesGroup):
    is_admin_menu = State()
    phone_number = State()
    fio = State()
    role = State()
    unit_id = State()
    admin_id = State()
    change_unit = State()
    change_phone_num = State()
    change_fio = State()
    business_unit_id = State()


class BusinessUnitState(StatesGroup):
    name = State()
    note = State()
    address = State()
    msg_id = State()
    unit_id = State()
    edit_field = State()
