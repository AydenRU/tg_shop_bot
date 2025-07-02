from gc import callbacks

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from model.select import get_list_products_db

__all__ = ['inline_main_button', 'inline_basket_button',
           'inline_admin_main_button', 'inline_product_button',
           'inline_item_product_button',
           'inline_admin_menu_button', 'inline_admin_add_product_button',
           'inline_admin_product_button', 'inline_admin_back_menu_edit_admin', 'inline_admin_product_button',
           'inline_admin_edit_product_admin', 'inline_admin_back_edit_product',
           'inline_admin_back_product']

# Главные кнопки доступные пользователю

inline_main_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Корзина', callback_data='Basket')],
                     [InlineKeyboardButton(text='Продукты', callback_data='Product')]])


inline_basket_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data='Del_product_in_bascet')],
                     [InlineKeyboardButton(text='Перейти к оплате', callback_data='pay_product_start')],
                     [InlineKeyboardButton(text='Назад', callback_data='start')]])


inline_product_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='start')]])


# inline_item_product_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='Product')]])



async def inline_item_product_button(id):
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.add(InlineKeyboardButton(text='Добавить в корзину', callback_data=f'Add_bascet_{id}'))
    inline_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='Product'))
    return inline_keyboard.adjust(1).as_markup()


async def inline_product_button():
    data = await get_list_products_db()
    button = InlineKeyboardBuilder()
    for i in data:
        button.add(InlineKeyboardButton(text=f'{i["nameproduct"]}\n{i["cost"]}', callback_data=f'product_{i["id"]}'))
    button.add(InlineKeyboardButton(text='Назад', callback_data='start'))
    return button.adjust(1).as_markup()


# Кнопки доступные администратору

inline_admin_main_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Корзина', callback_data='Basket')],
                     [InlineKeyboardButton(text='Продукты', callback_data='Product')],
                     [InlineKeyboardButton(text='Админ панель', callback_data='Admin')]]
    )




inline_admin_menu_button = InlineKeyboardMarkup(
    inline_keyboard=[
                     [InlineKeyboardButton(text='Список всех товаров', callback_data='Admin_edit_list_product')],
                     [InlineKeyboardButton(text='Назад', callback_data='start')]
                     ])



inline_admin_add_product_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data='Admin')]]
)


inline_admin_back_menu_edit_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить новый товар', callback_data='Add_new_or_else_product')],
    [InlineKeyboardButton(text='Удалить товар', callback_data='Admin_delete_product')],
    [InlineKeyboardButton(text='Изменить товар', callback_data='edit_product_admin')],
    [InlineKeyboardButton(text='Назад', callback_data='Admin')]
])


# Изменение продукта
inline_admin_edit_product_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить количество', callback_data='add_product_admin')],
    [InlineKeyboardButton(text='Уменьшить количество', callback_data='del_product_admin')],
    [InlineKeyboardButton(text='Изменить описание', callback_data='edit_description_admin')],
    [InlineKeyboardButton(text='Изменить стоимость', callback_data='edit_cost_admin')],
    [InlineKeyboardButton(text='Изменить фотографию', callback_data='edit_photo_admin')],
    [InlineKeyboardButton(text='Назад', callback_data='Admin_edit_list_product')]
])


inline_admin_back_edit_product = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='admin_back_edit_product')]
])


inline_admin_back_product = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data='Admin_edit_list_product')]
])


inline_admin_product_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='Admin')]])