from aiogram import Router

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from model.select import get_id_product, get_info_about_product_db

from model.change import admin_get_list_products_db

from Data.button import inline_admin_product_button, inline_admin_edit_product_admin

from Data.fsm_group import ProductNameEdit

router_edit_product_admin = Router()



async def select_edit_product_admin(id_product: int, state: FSMContext, target: Message | CallbackQuery):
    data_info = await get_info_about_product_db(id_product)

    await state.update_data(id_product=id_product)

    if isinstance(target, Message):
        await target.answer(text=f'_______________{data_info['nameproduct']}_______________\n'
                              f'Количество: {data_info['quantity']}\n'
                              f'Цена:   {data_info['cost']}\n'
                              f'Описание:   {data_info['description']}',
                         reply_markup=inline_admin_edit_product_admin)

    elif isinstance(target, CallbackQuery):
        await target.message.edit_text(text=f'_______________{data_info['nameproduct']}_______________\n'
                                 f'Количество: {data_info['quantity']}\n'
                                 f'Цена:   {data_info['cost']}\n'
                                 f'Описание:   {data_info['description']}',
                            reply_markup=inline_admin_edit_product_admin)



@router_edit_product_admin.callback_query(F.data == 'edit_product_admin')
async def edit_product_admin(callback: CallbackQuery, state: FSMContext):
    data = await admin_get_list_products_db()

    header = f"{'ID':<4}| {'name':<20}| {'quantity':<10}| {'cost':<10}| {'all_cost':<10}"
    lines = [header, "-" * len(header)]

    products_name = []
    # Формат каждой строки
    for item in data:
        products_name.append(item['nameproduct'])
        all_cost = item['quantity'] * item['cost']
        lines.append(
            f"{item['id']:<4}| {item['nameproduct']:<20}| {item['quantity']:<10}| {item['cost']:<10}| {all_cost:<10}"
        )
    text_data = "\n".join(lines)
    await state.set_state(ProductNameEdit.name)
    await state.update_data(products_name=products_name)

    await callback.message.edit_text(text=f'{text_data}\n Введи название продукта, которое хочешь изменить:', reply_markup=inline_admin_product_button)

@router_edit_product_admin.message(ProductNameEdit.name)
async def start_select_edit_product_admin(message: Message, state: FSMContext):
    products_name = (await state.get_data()).get('products_name')
    if message.text not in products_name:
        await message.answer(text='Данного продукта не существует. Введи правильно:', reply_markup=inline_admin_product_button)
        return
    await state.clear()

    id_product = await get_id_product(message.text)
    id_product = int(id_product['id'])

    await select_edit_product_admin(id_product, state, message)

@router_edit_product_admin.callback_query(F.data == 'admin_back_edit_product')
async def admin_back_edit_product(callback: CallbackQuery, state: FSMContext):
    id_product = (await state.get_data()).get('id_product')
    await select_edit_product_admin(id_product, state, callback)


