from aiogram import Router
from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from model.Edit.edit_product import admin_cost_products_edit_db

from Data.button import  inline_admin_back_edit_product

from Data.fsm_group import EditCost



router_cost_product = Router()

async def finish_cost_quantity(id_product: int, cost: float):
    await admin_cost_products_edit_db(id_product, cost)


async def converter_str_float(cost: str) -> float | None:
    simvols = (',/\\|.')
    result = None

    if cost.isdigit():
        result = round(float(cost), 2)
    else:
        for i in simvols:
            count = cost.count(i)
            if count == 1:
                value = cost.split(i)
                result = round(float('.'.join(value)), 2)
                break
            else:
                continue

    return result


@router_cost_product.callback_query(F.data == 'edit_cost_admin')
async def start_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите новую цену (12.41):?\n ', reply_markup=inline_admin_back_edit_product)
    await state.set_state(EditCost.cost)


@router_cost_product.message(EditCost.cost)
async def end_edd(message: Message, state: FSMContext):
    cost = await converter_str_float(message.text)

    if cost:
        id_product = (await state.get_data()).get('id_product')

        await finish_cost_quantity(id_product, cost)

        await message.answer(text='Цена изменена', reply_markup=inline_admin_back_edit_product)

    else:
        await message.answer(text='Неверно введено значение. Введите значение:', reply_markup=inline_admin_back_edit_product)
        return