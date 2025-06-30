import asyncio
from aiogram import Router

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from model.select import get_basket_db, get_quantity_basket, get_id_product
from model.change import put_basket_in_products_db, delete_basket_in_products_db

from fsm_group import DeleteProdictFromBasket

from requests.button import *

router_basket = Router()

async def render_basket(user_id: int, state: FSMContext, target: Message | CallbackQuery):
    """
    Отображает корзину пользователя, обновляет state.
    :target: — это сообщение или коллбэк, куда нужно отправить текст.
    """

    answer = await get_basket_db(user_id)
    text = ""
    name_product = {}

    for i in answer:
        name = i['nameproduct']
        quantity = int(i['quantity'])
        cost = float(i['cost'])
        total = quantity * cost

        name_product[i['nameproduct']] = quantity
        text += f"{name}: Кол: {quantity}, Цена.ед: {cost}, Цена: {total:.2f}\n"

    await state.update_data(text=text, products=name_product)

    if not text:
        text = "Ваша корзина пуста <3"

    # Определим, куда отправлять: callback или сообщение
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text=text, reply_markup=inline_basket_button)
    else:
        await target.answer(text=text, reply_markup=inline_basket_button)


@router_basket.callback_query(F.data == 'Basket')
async def basket(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик корзины с товарами покупателя
    """
    await render_basket(callback.from_user.id, state, callback)


@router_basket.callback_query(F.data.startswith('Del_product_in_bascet'))
async def delete_basket_in_product(callback: CallbackQuery, state: FSMContext):
    text = (await state.get_data()).get('text')

    await callback.message.edit_text(text=f'{text}Введите название товара: ')

    await state.set_state(DeleteProdictFromBasket.name)


@router_basket.message(DeleteProdictFromBasket.name)
async def delete_basket_in_product_quantity(message: Message, state: FSMContext):
    data = await state.get_data()


    if message.text not in data['products']:
        await message.answer(text=f'{data['text']}\n{message.text} нету в вашей корзине. Введите еще раз:')
        return

    await message.answer(text=f'{data['text']}\nВведите количество товара: ')

    await state.update_data(name=message.text)

    await state.set_state(DeleteProdictFromBasket.quantity)


@router_basket.message(DeleteProdictFromBasket.quantity)
async def delete_basket_in_product_final(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.text.isdigit():
        if int(message.text) >= data['products'][data['name']]:
            quantity = int(message.text)
            id_product = await get_id_product(data['name'])
            id_product = int(id_product['id'])
            await delete_basket_in_products_db(message.from_user.id, id_product, quantity)

        else:
            quantity = int(message.text)
            id_product = await get_id_product(data['name'])
            id_product = int(id_product['id'])
            await put_basket_in_products_db(message.from_user.id, id_product, quantity)


        msg = await message.answer("Удалили ✅")
        await asyncio.sleep(1)
        await msg.delete()

        await state.clear()
        await render_basket(message.from_user.id, state, message)
        return

    await message.answer(text=f'{data['text']}{message.text} неверно указано количество. Введите еще раз:')
    return

