from aiogram import Router


from aiogram.types import CallbackQuery
from aiogram import F

from requests.button import *

from model.select import get_info_about_product_db


router_product = Router()


@router_product.callback_query(F.data == 'Product')
async def catalog_product(callback: CallbackQuery):
    """
    Обработчик списка с доступными товарами
    """
    await callback.answer('')
    await callback.message.edit_text(text=f'Завтра сделаю вывод продуктов', reply_markup=await inline_product_button())


@router_product.callback_query(F.data.startswith('product_'))
async def info_product_shop(callback: CallbackQuery):
    """
    Обработчик подробной информации товара
    """
    id = callback.data[callback.data.find('_') + 1:]
    # print(id)
    data = await get_info_about_product_db(id)
    await callback.message.edit_text(text=f'_______________{data['nameproduct']}_______________\n'
                                          f'Количество: {data['quantity']}\n'
                                          f'Цена:   {data['cost']}\n'
                                          f'Описание:   {data['description']}', reply_markup=await inline_item_product_button(id))


@router_product.callback_query(F.data.startswith('Add_bascet_'))
async def add_product_in_basket(callback: CallbackQuery):
    id_product = int(callback.data[callback.data.rfind('_') + 1:])
    await products_in_baskets_db(callback.from_user.id, id_product)
    await callback.answer('Товар добавлен в корзину')