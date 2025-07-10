import asyncio
from aiogram import Router

from aiogram import F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from model.select import get_basket_db, get_id_product
from model.change import put_basket_in_products_db, delete_basket_in_products_db

from Data.fsm_group import DeleteProdictFromBasket

from Data.button import *

from utils.exceptions_dlia_my import ExceptionsCheck

router_basket = Router()


async def render_basket(user_id: int, state: FSMContext, target: Message | CallbackQuery):
    """
    Отображает корзину пользователя, обновляет state.
    :target: — это сообщение или коллбэк, куда нужно отправить текст.
    """

    answer = await get_basket_db(user_id)
    text = ""
    name_product = {}
    total_cost = 0
    for i in answer:
        name = i['nameproduct']
        quantity = int(i['quantity'])
        cost = float(i['cost'])
        total = quantity * cost
        total_cost += total
        name_product[i['nameproduct']] = quantity

        text += f"{name}: Кол: {quantity}, Цена.ед: {cost} руб., Цена: {total:.2f} руб.\n"

    await state.update_data(text=text, products=name_product)

    if not text:
        text = "Ваша корзина пуста <3"
    else:
        text += f"\nОбщая сумма:    {total_cost} руб."

    # await state.update_data(total_cost= total_cost)

    # Определим, куда отправлять: callback или сообщение
    if isinstance(target, CallbackQuery):
        await target.message.delete()
        await target.message.answer_photo(photo=FSInputFile("Data\\image\\basket.jpg") ,
                                  caption=text,
                                  reply_markup=inline_basket_button)
    else:
        await target.delete()
        await target.answer_photo(photo=FSInputFile("Data\\image\\basket.jpg") ,
                                  caption=text,
                                  reply_markup=inline_basket_button)


async def check_empty(callback: CallbackQuery, state: FSMContext):
    return True if not (await state.get_data()).get("text") else False


@router_basket.callback_query(F.data == 'Basket')
async def basket(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик корзины с товарами покупателя
    """
    await render_basket(callback.from_user.id, state, callback)


@router_basket.callback_query(F.data.startswith('Del_product_in_basket'))
@ExceptionsCheck.check_payment_status_pending
async def delete_basket_in_product(callback: CallbackQuery, state: FSMContext):
    text = (await state.get_data()).get('text')

    if await check_empty(callback, state):
        await render_basket(callback.from_user.id, state, callback)
        return

    await callback.message.delete()
    await callback.message.answer(text=f'{text}Введите название товара: ')

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

        msg = await message.answer("Удалили товар!!")
        await asyncio.sleep(1)

        await state.clear()
        await render_basket(message.from_user.id, state, message)
        return

    # await message.delete()
    await message.answer(text=f'{data['text']}{message.text} неверно указано количество. Введите еще раз:')
    return

