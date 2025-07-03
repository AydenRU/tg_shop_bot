from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Data.fsm_group import AddProduct

from model.change import admin_add_products_db

from Data.button import *



router_add_new_product_admin = Router()

@router_add_new_product_admin.callback_query(F.data == 'Add_new_or_else_product')
async def admin_add_product_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите название товара',
                                 reply_markup=inline_admin_add_product_button)
    await state.set_state(AddProduct.name)


@router_add_new_product_admin.message(AddProduct.name)
async def admin_add_product_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.answer(text='Введите цену за единицу товара',
                            reply_markup=inline_admin_add_product_button)
    await state.set_state(AddProduct.cost)


@router_add_new_product_admin.message(AddProduct.cost)
async def admin_add_product_threa(message: Message, state: FSMContext):
    await state.update_data(cost=f'{message.text}')
    await message.answer(text='Осталось ввести количество товара',
                         reply_markup=inline_admin_add_product_button)
    await state.set_state(AddProduct.quantity)


@router_add_new_product_admin.message(AddProduct.quantity)
async def admin_add_product_final(message: Message, state: FSMContext):
    name = await state.get_data()
    data = list(name.values()) + [message.text]
    await message.answer(text=f'Имя:{name['name']}\nСтоимость: {name['cost']}\n'
                              f'Количество: {message.text}',
                        reply_markup=inline_admin_add_product_button)
    await admin_add_products_db(data)
    await state.clear()
