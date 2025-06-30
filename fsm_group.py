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