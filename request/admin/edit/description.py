from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from model.select import get_quantity_product_db
from model.change import admin_del_products_db
from model.Edit.edit_product import admin_description_products_edit_db

from request.button import  inline_admin_back_edit_product, inline_admin_back_product

from fsm_group import EditDescription



router_description_product = Router()


async def finish_description(id_product: int, description: str):
    await admin_description_products_edit_db(id_product, description)


@router_description_product.callback_query(F.data == 'edit_description_admin')
async def start_del(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите новое описание: ', reply_markup=inline_admin_back_edit_product)
    await state.set_state(EditDescription.description)


@router_description_product.message(EditDescription.description)
async def end_del(message: Message, state: FSMContext):
    id_product = (await state.get_data()).get('id_product')

    if message.text:
        await finish_description(id_product, message.text)
        await message.answer(text='Описание изменено', reply_markup=inline_admin_back_edit_product)
    else:
        await message.answer(text='Описание не изменено', reply_markup=inline_admin_back_edit_product)
