from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Data.fsm_group import  DelProduct

from model.change import  admin_get_list_products_db, admin_del_products_db
from model.select import get_id_product

from Data.button import inline_admin_product_button

router_del_product_admin = Router()


@router_del_product_admin.callback_query(F.data == 'Admin_delete_product')
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
    await callback.message.edit_text(text=text_data, reply_markup=inline_admin_product_button)
    await state.set_state(DelProduct.name)


@router_del_product_admin.message(DelProduct.name)
async def admin_del_product(message: Message, state: FSMContext):
    name = message.text
    id_product = await get_id_product(name)
    id_product = id_product['id']

    await admin_del_products_db(id_product)
    await message.delete()
    await message.answer(text="Удаление произведено ", reply_markup=inline_admin_product_button)