import asyncio
import os

import uuid

import yookassa
from yookassa import Configuration, Payment

from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram.utils.keyboard import InlineKeyboardBuilder , InlineKeyboardButton

from dotenv import load_dotenv


from model.select import get_total_cost

load_dotenv()

Configuration.account_id = os.getenv("ACCOUNT_ID")
Configuration.secret_key = os.getenv('SECRET_KEY_PAY')

router_pay  = Router()



async def create(amount, id_users):

    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/AydenShopBot"
        },
        "capture": True,
        "metadata": {
            "chat_id": id_users
        },
        "description": "Заказ №1"
    }, uuid.uuid4())

    return payment.confirmation.confirmation_url, payment.id

@router_pay.callback_query(F.data == 'pay_product_start')
async def start_pay(callback: CallbackQuery):
    amount = await get_total_cost(callback.from_user.id)
    pay = await create(amount, callback.from_user.id)

    switching_to_payment = InlineKeyboardBuilder()
    switching_to_payment.add(InlineKeyboardButton(text='Оплатить', url=pay[0]))
    switching_to_payment.add(InlineKeyboardButton(text='Назад', callback_data='Basket'))

    await callback.message.answer(f'Оплата, на сумму {amount} ', reply_markup=switching_to_payment.as_markup())


