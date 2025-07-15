from aiogram import Router

from aiogram.types import CallbackQuery
from aiogram import F

from Data.button import *

from model.select import get_info_about_product_db
from model.change import products_in_baskets_db

from utils.exceptions_dlia_my import ExceptionsCheck


router_product = Router()


async def info_product_shop(callback, id_product):

    data = await get_info_about_product_db(id_product)
    if data['image'] is None:
        await callback.message.edit_text(text=f'_______________{data['nameproduct']}_______________\n'
                                            f'Количество: {data['quantity']}\n'
                                            f'Цена:   {data['cost']}\n'
                                            f'Описание:   {data['description']}',
                                       reply_markup=await inline_item_product_button(id_product))
    else:
        await callback.message.delete()
        await callback.message.answer_photo(photo=data['image'],
                                          caption=f'_______________{data['nameproduct']}_______________\n'
                                                  f'Количество: {data['quantity']}\n'
                                                  f'Цена:   {data['cost']}\n'
                                                  f'Описание:   {data['description']}',
                                          reply_markup=await inline_item_product_button(id_product))

@router_product.callback_query(F.data == 'Product')
async def catalog_product(callback: CallbackQuery):
    """
    Обработчик списка с доступными товарами
    """
    # await callback.answer('')
    await callback.message.delete()
    await callback.message.answer(text=f'Выберите интересуемый продукт.', reply_markup=await inline_product_button())


@router_product.callback_query(F.data.startswith('product_'))
async def handler_info_product_shop(callback: CallbackQuery):
    """
    Обработчик подробной информации товара
    """
    id_product = int(callback.data[callback.data.find('_') + 1:])
    await info_product_shop(callback, id_product)


@router_product.callback_query(F.data.startswith('Add_bascet_'))
@ExceptionsCheck.check_payment_status_pending
async def add_product_in_basket(callback: CallbackQuery):
    id_product = int(callback.data[callback.data.rfind('_') + 1:])
    await products_in_baskets_db(callback.from_user.id, id_product)
    await callback.answer('Товар добавлен в корзину')
    await info_product_shop(callback, id_product)