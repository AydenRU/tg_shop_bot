import aiogram

from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from model.Query_bd import new_user, get_basket_db, check_user
from aiogram.types import CallbackQuery

from requests.Button import *


router_admin = Router()

@router_admin.callback_query(F.data == 'Admin')
async def admin_interface(callback: CallbackQuery):
    await callback.message.edit_text(text=f'Приветствую администратор {callback.from_user.username}', reply_markup=inline_admin_menu_button)

@router_admin.callback_query(F.data == 'Admin_add_product')
async def admin_add_product(callback: CallbackQuery):
    pass

@router_admin.callback_query(F.data == 'Admin_delete_product')
async def admin_del_product(callback: CallbackQuery):
    pass

@router_admin.callback_query(F.data == 'Admin_edit_list_product')
async def admin_list_all_product(callback: CallbackQuery):
    pass

@router_admin.callback_query(F.data.startswith('Admin_edit_product'))
async def admin_show_product_for_edit(callback: CallbackQuery):
    pass

# admin_del_list_all_product