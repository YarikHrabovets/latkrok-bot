from aiogram import types
from constants import rent_names


main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
gallery = types.KeyboardButton('📑 Документи')
order = types.KeyboardButton('💲 Оренда')
logo = types.KeyboardButton('💲 Logo-килими')
sale = types.KeyboardButton('🚨 Акції')
contacts = types.KeyboardButton('📞 Контакти')
about_us = types.KeyboardButton('👥 Про нас')
profile = types.KeyboardButton('👤 Профіль')
main_menu.add(gallery, order, logo, sale, contacts, about_us, profile)


profile_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = types.KeyboardButton('📔 Мої товари')
back_to_main_menu = types.KeyboardButton('🔙 Головне меню')
profile_menu.add(items, back_to_main_menu)


cart_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
make_order = types.KeyboardButton('📝 Оформити замовлення')
cart_menu.add(make_order, back_to_main_menu)


empty_cart_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
do_shopping = types.KeyboardButton('🛍 Дивитися товари')
empty_cart_menu.add(do_shopping, back_to_main_menu)


colors = types.InlineKeyboardMarkup()
steel = types.InlineKeyboardButton('Сталь', callback_data='Сталь')
granite = types.InlineKeyboardButton('Граніт', callback_data='Граніт')
cedar = types.InlineKeyboardButton('Кедр', callback_data='Кедр')
colors.add(steel, granite, cedar)


def go_to_item(product_id: str):
    mark_up = types.InlineKeyboardMarkup()
    item = types.InlineKeyboardButton('Додати до кошика', callback_data=product_id)
    mark_up.add(item)

    return mark_up


def get_price_markup(price: dict):
    price_mark_up = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(f'{rent_names[i-1]} - {price[f"{i}"]}грн/міс',
                                          callback_data=f'{rent_names[i-1]} - {price[f"{i}"]}грн/міс') for i in range(1, len(price.items()))]
    price_mark_up.add(*buttons)

    return price_mark_up


def slider(value=1):
    chose_quantity = types.InlineKeyboardMarkup()
    minus = types.InlineKeyboardButton('-', callback_data=f'minus-{value}')
    current_value = types.InlineKeyboardButton(f'{value}/60', callback_data='do-nothing')
    plus = types.InlineKeyboardButton('+', callback_data=f'plus-{value}')
    add_to_cart = types.InlineKeyboardButton('🛒 Додати до кошика', callback_data='add-to-cart')
    chose_quantity.add(minus, current_value, plus, add_to_cart)

    return chose_quantity


def edit_cart(id_: int):
    mark_up = types.InlineKeyboardMarkup()
    mark_up.add(types.InlineKeyboardButton('Видалити', callback_data=f'delete-{id_}'))

    return mark_up


__all__ = ['main_menu', 'profile_menu', 'cart_menu', 'empty_cart_menu', 'go_to_item',
           'get_price_markup', 'colors', 'slider', 'edit_cart']
