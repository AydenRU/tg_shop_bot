from aiogram.fsm.state import State, StatesGroup



class DeleteProdictFromBasket(StatesGroup):
    name = State()
    quantity = State()

class AddProduct(StatesGroup):
    name = State()
    cost = State()
    quantity = State()

class DelProduct(StatesGroup):
    name = State()

class ProductNameEdit(StatesGroup):
    name = State()

class EditAddQuantity(StatesGroup):
    quantity = State()

class EditDelQuantity(StatesGroup):
    quantity = State()

class EditCost(StatesGroup):
    cost = State()

class EditDescription(StatesGroup):
    description = State()

class SelectUserOrder(StatesGroup):
    id_user = State()

class InputDataUsers(StatesGroup):
    first_name = State()
    last_name = State()
    address = State()
    contact_data = State()
