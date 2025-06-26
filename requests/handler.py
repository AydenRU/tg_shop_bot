import aiogram

from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


from model.Query_bd import new_user, get_basket_db
from aiogram.types import CallbackQuery

from requests.Button import *


router_main = Router()



@router_main.message(CommandStart())
async def start(message: Message):

    await new_user(message.from_user.id)
    await message.answer(f'Привет твои данные {message.from_user.id}, а имя {message.from_user.username} {message.from_user.first_name}',
                        reply_markup=inline_menu_button )

@router_main.callback_query(F.data == 'start')
async def back_to_start(callback: CallbackQuery):
    await callback.message.edit_text(
        f'Вы вернулись в главное меню.',
        reply_markup=inline_menu_button
    )
    await callback.answer()


@router_main.callback_query(F.data == 'Basket')
async def help(callback: CallbackQuery):

    answer = await get_basket_db(callback.from_user.id)
    text = ""
    for i in answer:
        text += f'{i['nameproduct']}:   {i['quantity']}  {i['cost'] * int(i['quantity'])}    {i['cost']}\n'

    if not text:
        text = 'Ваша корзина пуста <3'

    await callback.message.edit_text(text=f'{text}', reply_markup=inline_basket_button)

@router_main.callback_query(F.data == 'Product')
async def catalog_product(callback: CallbackQuery):

    await callback.answer('')
    await callback.message.edit_text(text=f'Завтра сделаю вывод продуктов', reply_markup=await inline_product_button())

@router_main.callback_query(F.data.startswith('product_'))
async def info_product(callback: CallbackQuery):
    id = callback.data[callback.data.find('_') + 1:]




