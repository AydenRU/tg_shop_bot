from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
