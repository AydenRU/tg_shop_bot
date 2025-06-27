from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from model.Query_bd import get_list_products_db

__all__ = ['inline_main_button', 'inline_basket_button', 'inline_admin_main_button', 'inline_product_button', 'inline_admin_menu_button']

# Главные кнопки доступные пользователю

inline_main_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Корзина', callback_data='Basket')],
                     [InlineKeyboardButton(text='Продукты', callback_data='Product')]])

inline_basket_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='start')]])

inline_product_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='start')]])


async def inline_product_button():
    data = await get_list_products_db()
    button = InlineKeyboardBuilder()
    for i in data:
        button.add(InlineKeyboardButton(text=f'{i['nameproduct']}\n{i['cost']}', callback_data=f'product_{i['id']}'))
    button.add(InlineKeyboardButton(text='Назад', callback_data='start'))
    return button.adjust(1).as_markup()

# Кнопки доступные администратору

inline_admin_main_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Корзина', callback_data='Basket')],
                     [InlineKeyboardButton(text='Продукты', callback_data='Product')],
                     [InlineKeyboardButton(text='Админ панель', callback_data='Admin')]]
    )

inline_admin_menu_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Добавить товар', callback_data='Add_new_or_else_product')],
                     [InlineKeyboardButton(text='Удалить товар', callback_data='Admin_delete_product')],
                     [InlineKeyboardButton(text='Список всех товаров', callback_data='Admin_edit_list_product')],
                     [InlineKeyboardButton(text='Назад', callback_data='start')]
                     ])
