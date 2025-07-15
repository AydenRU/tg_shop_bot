import os

import uuid
from types import NoneType

from aiogram.fsm.context import FSMContext
from yookassa import Configuration, Payment

from aiogram import Router, F
from aiogram.types import CallbackQuery

from utils.json_converter import json_basket

from aiogram.utils.keyboard import InlineKeyboardBuilder , InlineKeyboardButton

from dotenv import load_dotenv

from pay.user_data import input_first_name

from model.select import (
    get_total_cost,
    get_status_pending_payment,
    get_basket_db,
    get_is_order,
    get_status_payment,
    get_order_status
)
from model.change import (
    insert_info_payment,
    update_status,
    create_order,
    update_order,
    delete_basket_user
)

from Data.button import PaymentButton



load_dotenv()

Configuration.account_id = os.getenv("ACCOUNT_ID")
Configuration.secret_key = os.getenv('SECRET_KEY_PAY')

router_pay  = Router()

class StatusPayment:

    @staticmethod
    async def check_status(id_user: int) -> list[dict]:
        """
        Проверяет на платеж.
        Возвращает список с платежами
        :param id_user:
        :return: list[dict[status_payments, id_payments, url_pay]]
        """
        data = await get_status_pending_payment(id_user)
        pending = []

        for payment in data:
            check = Payment.find_one(payment['id_payments'])
            # print(check.status)
            if check.status == 'canceled':
                await update_status(id_user, payment['id_payments'], check.status)
            elif check.status == 'succeeded':
                await update_status(id_user, payment['id_payments'], check.status)

            else:
                pending.append(payment)

        return pending


    @staticmethod
    async def locker_payment(id_user: int) -> bool:
        return await get_is_order(id_user)



class CreatePayment:

    @staticmethod
    async def create(amount: float, id_users: int):
        """
        Создание платежа
        :param amount:
        :param id_users:
        :return:
        """
        return Payment.create({
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


class InteractionsPayment:

    @staticmethod
    async def return_payment_user(id_user) -> list[dict]:
        """
        Вернет данные о идущем платеже
        :param id_user:
        :return: Вернет словарь dict[status_payments, id_payments, url_pay]
        """

        return await get_status_pending_payment(id_user)


    @staticmethod
    async def create_payment(amount, id_users, state: FSMContext) -> dict | None:
        """
        Создание Оплату товара
        Если у тебя уже идёт оплата, то вернет ссылку на нынешнюю оплату.
        :param amount:
        :param id_users:
        :return: dict{'status': status[0]['status_payments'],
                    'id_payment': status[0]['id_payments'],
                    'url': status[0]['url_pay']
                    }
        """

        status = await StatusPayment.check_status(id_users)
        check_order = await StatusPayment.locker_payment(id_users)

        if not status and check_order:
            payment = await CreatePayment.create(amount, id_users)

            data_basket = await get_basket_db(id_users)

            await delete_basket_user(id_users)

            data_basket = await json_basket(data_basket)

            data_users = await state.get_data()

            await create_order(id_users, data_basket, data_users)

            await insert_info_payment(id_users, payment.id, payment.status,
                                      payment.confirmation.confirmation_url)

            return {'status': payment.status,
                    'id_payments': payment.id,
                    'url_pay': payment.confirmation.confirmation_url
                    }
        elif not check_order:
            return {}

        else:
            return {'status_payments': status[0]['status_payments'],
                    'id_payments': status[0]['id_payments'],
                    'url_pay': status[0]['url_pay']
                    }


@router_pay.callback_query(F.data == 'pay_check')
async def pay_check(callback: CallbackQuery):
    """
    Проверка состояния заказа
    :param callback:
    :return:
    """
    payment = await StatusPayment.check_status(callback.from_user.id)

    print(payment)
    if not payment:
        order = await get_order_status(callback.from_user.id)
        print(order)
        if order['order_status'] == 'Оплачивается':
            await update_order(callback.from_user.id, 'Собирается')
            await callback.message.edit_text(text=f'Ваш заказ находится на этапе - Собирается',
                                             reply_markup=await PaymentButton.inline_back_button())

        elif order :
            await callback.message.edit_text(text=f'Ваш заказ находится на этапе - {order['order_status']}',
                                             reply_markup=await PaymentButton.inline_back_button())

        else:
            await callback.message.edit_text(text='У вас нет действующих покупок',
                                         reply_markup=await PaymentButton.inline_back_button())

    else:
        await callback.message.edit_text(text=f"Заказ не оплачен, для оплаты перейдите по ссылке: "
                                           f"{payment[0]['url_pay']}", reply_markup=await PaymentButton.inline_back_button())


@router_pay.callback_query(F.data == 'create_task_payment')
async def create_task_payment(callback: CallbackQuery, state: FSMContext):
    """
    Старк платежа и вывод данных
    :param state:
    :param callback:
    :return:
    """
    id_user = callback.from_user.id
    amount = await get_total_cost(id_user)

    payment = await InteractionsPayment.create_payment(amount, id_user, state)

    if payment:
        await callback.message.edit_text(text=f'К оплате сумма в размере : {amount} Рублей.\n'
                                              f'Перейдите по ссылке для оплаты товара: \n'
                                              f'{payment["url_pay"]}',
                                         reply_markup=await PaymentButton.inline_back_button())
    else:
        await callback.message.edit_text(
            text=f'Вы не можете создать новый заказ, пока не получите уже оплаченный заказ',
            reply_markup=await PaymentButton.inline_back_button())

    await state.clear()


# @router_pay.callback_query(F.data == 'pay_cancel')
# async def payment_cancel(callback: CallbackQuery):
#     await callback.message.edit_text(text='Данный метод не работает так как не поддерживается тестовым магазином',
#                                      reply_markup=await PaymentButton.inline_back_button())
    # id_users = callback.from_user.id
    # id_payment = await get_status_payment(id_users)
    # idempotence_key = str(uuid.uuid4())
    # print(id_payment['id_payments'])
    # id_payment = await get_status_payment(id_users)
    #
    # payment = Payment.find_one(id_payment['id_payments'])

    # if payment.status == "pending":
    #     cancelled_payment = payment.cancel(idempotency_key=str(uuid.uuid4()))
    #     print(cancelled_payment.status)
    #     await callback.message.edit_text(text='Оплата отменена',
    #                                      reply_markup=await PaymentButton.inline_back_button())
    # else:
    #     await callback.message.edit_text(text='Не получилось',
    #                                      reply_markup=await PaymentButton.inline_back_button())


@router_pay.callback_query(F.data == 'check_basket_users')
async def check_basket_not_empty_users(callback: CallbackQuery, state: FSMContext):
    """
    перед началом оплаты проверка на наличие товара к оплате
    :param callback:
    :param state:
    :return:
    """
    id_user = callback.from_user.id
    amount = await get_total_cost(id_user)

    if amount  :
        await input_first_name(callback, state)

    else:
        await callback.message.edit_text(text=f'Ваша корзина пуста. Положите в нее товар.',
                                      reply_markup=await PaymentButton.inline_back_button())


@router_pay.callback_query(F.data == 'pay_product_start')
async def start_pay(callback: CallbackQuery):
    switching_to_payment = InlineKeyboardBuilder()
    switching_to_payment.add(InlineKeyboardButton(text='Оплатить', callback_data='check_basket_users'))
    switching_to_payment.add(InlineKeyboardButton(text='Проверить заказ', callback_data='pay_check'))
    # switching_to_payment.add(InlineKeyboardButton(text='Отменить заказ()', callback_data='pay_cancel'))
    switching_to_payment.add(InlineKeyboardButton(text='Назад', callback_data='Basket'))

    await callback.message.delete()
    await callback.message.answer(text=f'Добро пожаловать в окно оплаты товара ',
                                  reply_markup=switching_to_payment.adjust(1).as_markup())