from aiogram  import Router

from aiogram import F
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext



router_support_message = Router()

@router_support_message.callback_query(F.data == 'admin_support')
async def simple_