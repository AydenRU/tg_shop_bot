import asyncio

from aiogram import Router

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from Data.fsm_group import SelectUserOrder
from Data.button import Orders

from model.select import  get_data_order_users


main_list_order_router =  Router()

async def generator_text_order(data_orders: list[dict]) -> str:
    text = f'{"id":<5}|{"id_users":<25}|{"order_status":<25}\n'
    text += ('=' * len(text)) + '\n'

    for order in data_orders:
        text += (f'{order["id"]:<5}|{order["id_users"]:<25}|{order["order_status"]:<25}\n')
        await asyncio.sleep(0)

    return text

@main_list_order_router.callback_query(F.data == 'main_list_order')
async def main_list_order(callback: CallbackQuery, state: FSMContext):
    data_orders = await get_data_order_users()  # Запрашиваем данные пользователей\
    await callback.message.delete()
    await callback.message.answer(text=f'{await generator_text_order(data_orders)}'
                                       f'\nЕсли хотите посмотреть пользователя введите его id_users:',
                                  reply_markup=await Orders.inline_back_button())
    await state.set_state(SelectUserOrder.id_user)


