from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from model.select import get_quantity_product_db
from model.change import admin_del_products_db
from model.Edit.edit_product import admin_del_products_edit_db

from requests.button import  inline_admin_back_edit_product, inline_admin_back_product

from fsm_group import EditDelQuantity



router_del_product = Router()

async def finish_del_quantity(id_product: int, quantity: int):
    await admin_del_products_edit_db(id_product, quantity)


@router_del_product.callback_query(F.data == 'del_product_admin')
async def start_del(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Сколько удалить?\nВведите: ', reply_markup=inline_admin_back_edit_product)
    await state.set_state(EditDelQuantity.quantity)


@router_del_product.message(EditDelQuantity.quantity)
async def end_del(message: Message, state: FSMContext):
    id_product = (await state.get_data()).get('id_product')
    db_quantity = await get_quantity_product_db(id_product)
    db_quantity = int(db_quantity['quantity'])

    if message.text.isdigit() and int(message.text) < db_quantity:
        quantity = int(message.text)


        await finish_del_quantity(id_product, quantity)
        await message.answer(text='Удалено указанное количество товара', reply_markup=inline_admin_back_edit_product)

    elif message.text.isdigit() and int(message.text) == db_quantity:
        await admin_del_products_db(id_product)
        await message.answer(text='Товар удален', reply_markup=inline_admin_back_product)

    else:
        await message.answer(text='Неверно введено значение. Введите значение:', reply_markup=inline_admin_back_edit_product)
        return