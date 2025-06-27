import aiogram

from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import CallbackQuery, Message

from model.Query_bd import admin_add_products_db

from requests.Button import *

class Add_product(StatesGroup):
    name = State()
    cost = State()
    quantity = State()

router_admin = Router()

@router_admin.callback_query(F.data == 'Admin')
async def admin_interface(callback: CallbackQuery):
    await callback.message.edit_text(text=f'Приветствую администратор {callback.from_user.username}',
                                     reply_markup=inline_admin_menu_button)


@router_admin.callback_query(F.data == 'Add_new_or_else_product')
async def admin_add_product_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите название товара',
                                 reply_markup=inline_admin_add_product_button)
    await state.set_state(Add_product.name)

@router_admin.message(Add_product.name)
async def admin_add_product_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.answer(text='Введите цену за единицу товара',
                            reply_markup=inline_admin_add_product_button)
    await state.set_state(Add_product.cost)

@router_admin.message(Add_product.cost)
async def admin_add_product_threa(message: Message, state: FSMContext):
    await state.update_data(cost=f'{message.text}')
    await message.answer(text='Осталось ввести количество товара',
                         reply_markup=inline_admin_add_product_button)
    await state.set_state(Add_product.quantity)

@router_admin.message(Add_product.quantity)
async def admin_add_product_final(message: Message, state: FSMContext):
    name = await state.get_data()
    data = list(name.values()) + list(message.text)
    await message.answer(text=f'Имя:{name['name']}\nСтоимость: {name['cost']}\n'
                              f'Количество: {message.text}',
                        reply_markup=inline_admin_add_product_button)
    await admin_add_products_db(data)
    await state.clear()

@router_admin.callback_query(F.data == 'Admin_delete_product')
async def admin_del_product(callback: CallbackQuery):
    pass

@router_admin.callback_query(F.data == 'Admin_edit_list_product')
async def admin_list_all_product(callback: CallbackQuery):
    pass

@router_admin.callback_query(F.data.startswith('Admin_edit_product'))
async def admin_show_product_for_edit(callback: CallbackQuery):
    pass

# admin_del_list_all_product