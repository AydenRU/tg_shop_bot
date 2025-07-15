from aiogram import Router

import re


from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Data.fsm_group import InputDataUsers

from Data.button import PaymentButton, GetData

user_data_router = Router()

def check_symbol(name: str):
    prefix = set(r' !@#$%^&*()_-:+?><,./\|')
    name = set(name)
    result = prefix.intersection(name)

    return True if result else False

async def check_contact(contact: str):
    #Проверяем первый символ и на его основе понимаем, что за данные

    check = {
        '+': lambda x: x.isdigit(),
        '@': lambda x: re.fullmatch(r'^[a-zA-Z0-9_]{5,32}$', x) is not None
    }

    for sign, func in check.items():
        if contact[0] == sign:
            return func(contact[1:])

    return False


async def check_data(data: dict, message: Message, state: FSMContext):
    pass


async def input_first_name(callback: CallbackQuery, state: FSMContext):
    """
    Ввод имени
    :param callback:
    :param state:
    :return:
    """
    await callback.message.answer(text='Для отплаты товара заполните следующие данные')
    await callback.message.answer(text='Введите ваше имя :',
                                  reply_markup=await PaymentButton.inline_back_button())
    await state.set_state(InputDataUsers.first_name)


@user_data_router.message(InputDataUsers.first_name)
async def input_last_name(message: Message, state: FSMContext):
    """
    Ввод фамилии
    :param message:
    :param state:
    :return:
    """
    if check_symbol(message.text):
        await message.answer(text='Недопустимые символы\n'
                                  'Введите заново',
                             reply_markup=await PaymentButton.inline_back_button())
        return
    else:
        await state.update_data(first_name=message.text.capitalize() )
        await message.answer(text='Введите вашу фамилию :',
                             reply_markup=await PaymentButton.inline_back_button())
        await state.set_state(InputDataUsers.last_name)


@user_data_router.message(InputDataUsers.last_name)
async def input_address(message: Message, state: FSMContext):
    """
    Ввод адреса доставки
    :param message:
    :param state:
    :return:
    """
    if check_symbol(message.text):
        await message.answer(text='Недопустимые символы\n'
                                  'Введите заново',
                             reply_markup=await PaymentButton.inline_back_button())
        return
    else:
        await state.update_data(last_name=message.text.capitalize() )
        await message.answer(text='Введите адрес доставки заказа:',
                             reply_markup=await PaymentButton.inline_back_button())
        await state.set_state(InputDataUsers.address)


@user_data_router.message(InputDataUsers.address)
async def input_contact_data(message: Message, state: FSMContext):
    """
    Ввод контактных данных
    :param message:
    :param state:
    :return:
    """
    await state.update_data(address=message.text )
    await message.answer(text='Введите контактные данные (телефон/ссылка TG):',
                         reply_markup=GetData.reply_take_phone())
    await state.set_state(InputDataUsers.contact_data)



@user_data_router.message(InputDataUsers.contact_data, F.contact | F.text)
async def to_go_create_payment(message: Message, state: FSMContext):
    """Вывод введенных данных для пользователя """
    if message.contact:
        contact_info = message.contact.phone_number


    else:
        contact_info = message.text.strip()
        phone_pattern = r'^(\+7|8)\d{10}$'

        if re.fullmatch(phone_pattern, contact_info):
            await state.update_data(contact_data=contact_info)

        else:
            await message.answer("Пожалуйста, введите корректный номер"
                                 " телефона в формате +7XXXXXXXXXX или 8XXXXXXXXXX")
            return

    await state.update_data(contact_data=contact_info)


    data = await state.get_data()

    text = (
        f'Проверьте данные\n\n'
        f'Фамилия и имя: {data.get("last_name")} {data.get("first_name")}\n'
        f'Адрес: {data.get("address")}\n'
        f'Контактные данные: {data.get("contact_data")}\n\n'
        f'Если всё верно — нажмите кнопку "Продолжить".'
    )
    print(data)
    await message.answer(text=text,
                         reply_markup=await PaymentButton.inline_to_go_payment())

