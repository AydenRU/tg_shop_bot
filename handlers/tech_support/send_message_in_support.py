from aiogram import Router
import re

from aiogram import F
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext

from model.change import SupportBD

from pay.user_data import GetData
from Data.fsm_group import MessageInSupport

from Data.button import SupportButton

router_send_message_in_support = Router()

@router_send_message_in_support.callback_query(F.data == 'send_message_in_support')
async def send_message_in_support(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Добрый день, если у вас возникнут вопросы.\n'
                                       'Напишите ваш вопрос. С вами свяжутся в ближайшее время ',
                                  reply_markup=await SupportButton.inline_back_main_button())

    await state.set_state(MessageInSupport.text)


@router_send_message_in_support.message(MessageInSupport.text)
async def input_text_support(message: Message, state: FSMContext):

    await message.delete()
    await message.answer(text='Введите контактные данные',
                         reply_markup=GetData.reply_take_phone())
    await state.update_data(text=message.text)
    await state.set_state(MessageInSupport.contact_data)


@router_send_message_in_support.message(MessageInSupport.contact_data)
async def input_contact_data(message: Message, state: FSMContext):
    if message.contact:
        contact_info = message.contact.phone_number

    else:
        contact_info = message.text.strip()
        phone_pattern = r'^(\+7|8)\d{10}$'

        if re.fullmatch(phone_pattern, contact_info):
            await state.update_data(contact_data=contact_info)

        else:
            await message.answer("Пожалуйста, введите корректный номер"
                                 "телефона в формате +7XXXXXXXXXX или 8XXXXXXXXXX")
            return

    await SupportBD.send_support(message.from_user.id, (await state.get_data()).get('text'), contact_info)

    await message.delete()
    await state.clear()
    await message.answer(text='Ваша заявка отправлена. С вами свяжутся.',
                         reply_markup=await SupportButton.inline_back_main_button())