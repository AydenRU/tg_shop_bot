import asyncio

from aiogram import Router

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.json_converter import json_in_list

from Data.fsm_group import SelectUserOrder


from model.select import get_data_order_user
from model.change import update_order

from Data.button import Orders



edit_order_router = Router()


async def generator_info_order(data_about_user: dict, order_data: list[dict]):
    text = (f"ID пользователя: {data_about_user['id']}\n"
            f"Заказ оплачен : {data_about_user['start_time']}\n"
            f"Заказ находится в статусе: {data_about_user['order_status']}"
            f"Список заказа:\n"
            f"{'Имя товара':<10}|{'Количество':<10}|{'Цена за ед.':<10}|{'Сумма':<10}\n\n")

    total = 0
    for item in order_data:
        sum_cost = item['cost'] * item['quantity']
        text += f"{item['name_product']:<10}|{item['quantity']:<10}|{item['cost']:<10}|{sum_cost:<10}\n"
        total += sum_cost

    text += f"\n\n Общаая сумма: {total} рублей"

    return text


async def main_select_orders(target: Message | CallbackQuery, state: FSMContext):
    await state.clear()

    if isinstance(target, Message):
        data_about_user = await get_data_order_user(target.from_user.id)    # Запрашиваются данные об заказе пользователя
        order_data = json_in_list(data_about_user['order_data'])

        text = await generator_info_order(data_about_user, order_data)

        await state.update_data(id_user=data_about_user['id_users'], status=data_about_user['order_status'])
        await target.answer(text=text, reply_markup=await Orders.inline_main_select_orders())

    else:
        data_about_user = await get_data_order_user(target.from_user.id) # Запрашиваются данные об заказе пользователя
        order_data = json_in_list(data_about_user['order_data'])
        text = await generator_info_order(data_about_user, order_data)
        await state.update_data(id_user=data_about_user['id_users'], status=data_about_user['order_status'])
        await target.message.answer(text=text, reply_markup=await Orders.inline_main_select_orders())


@edit_order_router.message(SelectUserOrder.id_user)
async def main_edit_orders(message: Message, state: FSMContext):
    await main_select_orders(message, state)


@edit_order_router.callback_query(F.data == 'up_grayed_order')
async def up_grayed_order(callback: CallbackQuery, state: FSMContext):
    """
    Повышает статус на единицу.
    Принимает статусы: 'Собирается', 'В пути'
    :param callback:
    :param state:
    :return:
    """
    start_data= await state.get_data()
    print(start_data)

    try:
        if start_data['status'] == 'Доставлен':
            await callback.message.answer(text='Этот уровень повышен до максимального')
            await asyncio.sleep(3)
            await callback.message.delete()
            raise ValueError('В запросе на повышение статуса не может быть: "Доставлен"')
    except ValueError as error:
        print(f'ValueError: {error}')
        return

    status = ('Собирается', 'В пути', 'Доставлен') # Данные в БД расположены в таком же порядке
    for index_state in range(len(status)):
        print(status, '\n', index_state, '\n', status[index_state], '\n', start_data['status'])
        if status[index_state] == start_data['status']:
            await update_order(callback.from_user.id, status[index_state + 1]) # Здесь должен быть запрос на повышение грейда на один уровень
            print('статус повышен')
            break
    else:
        print('я по приколу')

    await callback.message.delete()
    await main_select_orders(callback, state)