from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from fsm_group import AddProduct, DelProduct

from model.change import admin_add_products_db, admin_get_list_products_db, admin_del_products_db
from model.select import get_id_product

from requests.button import *



router_admin = Router()

@router_admin.callback_query(F.data == 'Admin')
async def admin_interface(callback: CallbackQuery):
    await callback.message.edit_text(text=f'Приветствую администратор {callback.from_user.username}',
                                     reply_markup=inline_admin_menu_button)


@router_admin.callback_query(F.data == 'Add_new_or_else_product')
async def admin_add_product_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите название товара',
                                 reply_markup=inline_admin_add_product_button)
    await state.set_state(AddProduct.name)


@router_admin.message(AddProduct.name)
async def admin_add_product_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.answer(text='Введите цену за единицу товара',
                            reply_markup=inline_admin_add_product_button)
    await state.set_state(AddProduct.cost)


@router_admin.message(AddProduct.cost)
async def admin_add_product_threa(message: Message, state: FSMContext):
    await state.update_data(cost=f'{message.text}')
    await message.answer(text='Осталось ввести количество товара',
                         reply_markup=inline_admin_add_product_button)
    await state.set_state(AddProduct.quantity)


@router_admin.message(AddProduct.quantity)
async def admin_add_product_final(message: Message, state: FSMContext):
    name = await state.get_data()
    data = list(name.values()) + [message.text]
    await message.answer(text=f'Имя:{name['name']}\nСтоимость: {name['cost']}\n'
                              f'Количество: {message.text}',
                        reply_markup=inline_admin_add_product_button)
    await admin_add_products_db(data)
    await state.clear()


@router_admin.callback_query(F.data == 'Admin_delete_product')
async def admin_list_del_product(callback: CallbackQuery, state: FSMContext):
    data = await admin_get_list_products_db()

    header = f"{'ID':<4}| {'name':<20}| {'quantity':<10}| {'cost':<10}| {'all_cost':<10}"
    lines = [header, "-" * len(header)]  # Добавим линию под заголовком

    # Формат каждой строки
    for item in data:
        all_cost = item['quantity'] * item['cost']
        lines.append(
            f"{item['id']:<4}| {item['nameproduct']:<20}| {item['quantity']:<10}| {item['cost']:<10}| {all_cost:<10}"
        )

    text_data = "\n".join(lines)
    text_data += '\n\nВведите имя продукта, которое хотите удалить!!'
    await callback.message.edit_text(text=text_data, reply_markup=inline_admin_back_admin)
    await state.set_state(DelProduct.name)


@router_admin.message(DelProduct.name)
async def admin_del_product(message: Message, state: FSMContext):
    name = message.text
    id = int(await get_id_product(name))
    await admin_del_products_db(id)
    await message.edit_text(text="Удаление произведено ", reply_markup=inline_admin_back_admin)


@router_admin.callback_query(F.data == 'Admin_edit_list_product')
async def admin_list_all_product(callback: CallbackQuery):
    data = await admin_get_list_products_db()
    # text_data = ['ID  |       name        |   quantity    |   cost    |   all_cost\n']
    # print(data)
    # for i in data:
    #     text_data.append(f'{i['id']} | {i['nameproduct']}    |{i['quantity']}    |{i['cost']}    | {i['quantity'] * i['cost']}\n')

    header = f"{'ID':<4}| {'name':<20}| {'quantity':<10}| {'cost':<10}| {'all_cost':<10}"
    lines = [header, "-" * len(header)]

    # Формат каждой строки
    for item in data:
        all_cost = item['quantity'] * item['cost']
        lines.append(
            f"{item['id']:<4}| {item['nameproduct']:<20}| {item['quantity']:<10}| {item['cost']:<10}| {all_cost:<10}"
        )

    text_data = "\n".join(lines)
    await callback.message.edit_text(text=text_data, reply_markup=inline_admin_back_admin)


@router_admin.callback_query(F.data.startswith('Admin_edit_product'))
async def admin_show_product_for_edit(callback: CallbackQuery):
    pass

