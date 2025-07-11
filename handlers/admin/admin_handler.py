from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from model.change import  admin_get_list_products_db

from Data.button import *



router_admin = Router()

@router_admin.callback_query(F.data == 'Admin')
async def admin_interface(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer_photo(photo=FSInputFile("Data\\image\\admin.jpg"),
                                        text=f'Приветствую администратор {callback.from_user.username}',
                                        reply_markup=inline_admin_menu_button)


@router_admin.callback_query(F.data == 'Admin_edit_list_product')
async def admin_list_all_product(callback: CallbackQuery, state: FSMContext):
    data = await admin_get_list_products_db()
    await state.clear() # Все не нужное из нижних уровней

    header = f"{'ID':<4}| {'name':<20}| {'quantity':<10}| {'cost':<10}| {'all_cost':<10}"
    lines = [header, "-" * len(header)]

    # Формат каждой строки
    for item in data:
        all_cost = item['quantity'] * item['cost']
        lines.append(
            f"{item['id']:<4}| {item['nameproduct']:<20}| {item['quantity']:<10}| {item['cost']:<10}| {all_cost:<10}"
        )

    text_data = "\n".join(lines)
    await callback.message.delete()
    await callback.message.answer(text=text_data, reply_markup=inline_admin_back_menu_edit_admin)


