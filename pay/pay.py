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


from model.select import get_total_cost, get_status_payment, get_status_pending_payment
from model.change import insert_info_payment, update_status

load_dotenv()

Configuration.account_id = os.getenv("ACCOUNT_ID")
Configuration.secret_key = os.getenv('SECRET_KEY_PAY')

router_pay  = Router()

async def get_payment_info_from_db(id_users) -> dict:
    return await get_status_pending_payment(id_users)


async def check_status(id_user):
    data = await get_status_pending_payment(id_user)
    results =  []
    for i in data:
        check = Payment.find_one(i['id_payments'])
        # print(check.status)
        if check.status == 'canceled':
            await update_status(id_user, i['id_payments'], check.status)
        elif check.status == 'succeeded':
            await update_status(id_user, i['id_payments'], check.status)
        else:
            results.append(i['url_pay'])
    return results


async def create(amount, id_users):
    """
    Создание Оплату товара
    Если у тебя уже идёт оплата, то вернет ссылку на нынешнюю оплату.
    :param amount:
    :param id_users:
    :return:
    """
    # await get_payment_info_from_db(id_users)

    check_pay = await check_status(id_users)

    if not check_pay:
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
            "test": True,
            "metadata": {
                "chat_id": id_users
            },
            "description": "Заказ №1"
        }, uuid.uuid4())

        await insert_info_payment(id_users, payment.id, payment.status,
                                  payment.confirmation.confirmation_url)

        return payment.confirmation.confirmation_url

    else:
        result = [i['url_pay'] for i in check_pay]
        return result


@router_pay.callback_query(F.data == 'pay_check')
async def pay_check(callback: CallbackQuery):
    url = await check_status(callback.from_user.id)
    if len(url) == 0:
        await callback.message.answer(text='У вас нет действующих покупок')
    else:
        print(url)
        url = " ".join(url)
        await callback.message.answer(text=url)


@router_pay.callback_query(F.data == 'create_task_payment')
async def create_task_payment(callback: CallbackQuery):
    id_user = callback.from_user.id
    amount = await get_total_cost(id_user)

    text = await create(amount, id_user)

    if isinstance(text, list):
        text = " ".join(text)

    await callback.message.answer(text=text)


@router_pay.callback_query(F.data == 'pay_product_start')
async def start_pay(callback: CallbackQuery):
    switching_to_payment = InlineKeyboardBuilder()
    switching_to_payment.add(InlineKeyboardButton(text='Оплатить', callback_data='create_task_payment'))
    switching_to_payment.add(InlineKeyboardButton(text='Проверить заказ', callback_data='pay_check'))
    switching_to_payment.add(InlineKeyboardButton(text='Назад', callback_data='Basket'))

    await callback.message.answer(f'Оплата, на сумму {await get_total_cost(callback.from_user.id)} ',
                                  reply_markup=switching_to_payment.as_markup())




