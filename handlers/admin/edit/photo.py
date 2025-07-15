from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from model.Edit.edit_product import admin_photo_products_edit_db

from Data.button import  inline_admin_back_edit_product

from Data.fsm_group import EditPhoto



router_photo_product = Router()


async def finish_photo(id_product: int, photo: str):
    await admin_photo_products_edit_db(id_product, photo)


@router_photo_product.callback_query(F.data == 'edit_photo_admin')
async def start_del(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='отправьте новое изображение ', reply_markup=inline_admin_back_edit_product)
    await state.set_state(EditPhoto.photo)


@router_photo_product.message(EditPhoto.photo)
async def end_del(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer(text='Это не изображение. Попробуйте снова',
                             reply_markup=inline_admin_back_edit_product)
        return
    else:
        id_product = (await state.get_data()).get('id_product')
        await finish_photo(id_product, message.photo[-1].file_id)
        await message.answer(text='Фотография изменена', reply_markup=inline_admin_back_edit_product)