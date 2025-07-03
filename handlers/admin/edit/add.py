from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from model.Edit.edit_product import admin_add_products_edit_db

from Data.button import  inline_admin_back_edit_product

from Data.fsm_group import EditAddQuantity



router_add_product = Router()

async def finish_add_quantity(id_product: int, quantity: int):
    await admin_add_products_edit_db(id_product, quantity)


@router_add_product.callback_query(F.data == 'add_product_admin')
async def start_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Сколько добавить?\nВведите: ', reply_markup=inline_admin_back_edit_product)
    await state.set_state(EditAddQuantity.quantity)


@router_add_product.message(EditAddQuantity.quantity)
async def end_edd(message: Message, state: FSMContext):
    if message.text.isdigit():
        quantity = int(message.text)
        id_product = (await state.get_data()).get('id_product')

        await finish_add_quantity(id_product, quantity)
        await message.answer(text='Продукт добавлен', reply_markup=inline_admin_back_edit_product)

    else:
        await message.answer(text='Неверно введено значение. Введите значение:', reply_markup=inline_admin_back_edit_product)
        return