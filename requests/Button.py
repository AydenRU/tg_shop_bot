from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from model.Query_bd import get_list_products_db

__all__ = ['inline_menu_button', 'inline_boba_button', 'inline_basket_button', 'inline_product_button']



inline_menu_button  = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Корзина', callback_data='Basket')],
                                    [InlineKeyboardButton(text='Продукты', callback_data='Product')]])


inline_boba_button = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Крутая кнопка', callback_data='start'),
        InlineKeyboardButton(text='Еще более крутая кнопка', callback_data='start')]])

inline_basket_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='start')]])

inline_product_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='start')]])


async def inline_product_button():
    data = await get_list_products_db()
    button = InlineKeyboardBuilder()
    for i in data:
        button.add(InlineKeyboardButton(text=f'{i['nameproduct']}\n{i['cost']}', callback_data=f'product_{i['id']}'))
    button.add(InlineKeyboardButton(text='Назад', callback_data='start'))
    return button.adjust(1).as_markup()
