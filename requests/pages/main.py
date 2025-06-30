from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from model.status import CheckStatus

from requests.button import *

router_main = Router()



@router_main.message(CommandStart())
async def start(message: Message):
    """
    Обработчик первого входа пользователя в главное меню
    """
    check = await CheckStatus.check_user(message.from_user.id)

    # photo = FSInputFile()

    if check:
        keybord = inline_admin_main_button
    else:
        keybord = inline_main_button

    await CheckStatus.check_user(message.from_user.id)
    await message.answer(f'Привет твои данные {message.from_user.id}, а имя {message.from_user.username} {message.from_user.first_name}',
                        reply_markup=keybord )

@router_main.callback_query(F.data == 'start')
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик входа пользователя в главное меню
    """
    await state.clear()
    check = await CheckStatus.check_user(callback.from_user.id)

    if check:
        keybord = inline_admin_main_button
    else:
        keybord = inline_main_button

    await callback.message.edit_text(
        f'Вы вернулись в главное меню.',
        reply_markup=keybord
    )
    await callback.answer()



