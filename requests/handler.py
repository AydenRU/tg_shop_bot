import aiogram

from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove


from model.Query_bd import new_user, get_basket_db, check_user
from aiogram.types import CallbackQuery

from requests.Button import *


router_main = Router()



@router_main.message(CommandStart())
async def start(message: Message):
    """
    Обработчик первого входа пользователя в главное меню
    """
    check = await check_user(message.from_user.id)
    if check:
        keybord = inline_admin_main_button
    else:
        keybord = inline_main_button

    await new_user(message.from_user.id)
    await message.answer(f'Привет твои данные {message.from_user.id}, а имя {message.from_user.username} {message.from_user.first_name}',
                        reply_markup=keybord )

@router_main.callback_query(F.data == 'start')
async def back_to_start(callback: CallbackQuery):
    """
    Обработчик входа пользователя в главное меню
    """
    check = await check_user(callback.from_user.id)
    if check:
        keybord = inline_admin_main_button
    else:
        keybord = inline_main_button

    await callback.message.edit_text(
        f'Вы вернулись в главное меню.',
        reply_markup=keybord
    )
    await callback.answer()


@router_main.callback_query(F.data == 'Basket')
async def basket(callback: CallbackQuery):
    """
    Обработчик корзины с товарами покупателя
    """
    answer = await get_basket_db(callback.from_user.id)
    text = ""
    for i in answer:
        text += f'{i['nameproduct']}:   {i['quantity']}  {i['cost'] * int(i['quantity'])}    {i['cost']}\n'

    if not text:
        text = 'Ваша корзина пуста <3'

    await callback.message.edit_text(text=f'{text}', reply_markup=inline_basket_button)

@router_main.callback_query(F.data == 'Product')
async def catalog_product(callback: CallbackQuery):
    """
    Обработчик списка с доступными товарами
    """
    await callback.answer('')
    await callback.message.edit_text(text=f'Завтра сделаю вывод продуктов', reply_markup=await inline_product_button())

@router_main.callback_query(F.data.startswith('product_'))
async def info_product(callback: CallbackQuery):
    """
    Обработчик подробной информации товара
    """
    id = callback.data[callback.data.find('_') + 1:]






