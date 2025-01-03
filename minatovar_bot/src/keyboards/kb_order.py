from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from .kb_client import cancel_b

create_order_b = KeyboardButton(text="Сделать заказ")
my_orders_b = KeyboardButton(text="Мои заказы")

confrim_b = KeyboardButton(text="Да всё верно")


def order_menu_inline():
    create_order_b = InlineKeyboardButton(
        text="Сделать заказ", callback_data="createorder"
    )
    my_orders_b = InlineKeyboardButton(text="Мои заказы", callback_data="myorders")
    menu_b = InlineKeyboardButton(text="Меню", callback_data="menu")

    bottons = [[create_order_b, my_orders_b], [menu_b]]
    return InlineKeyboardMarkup(inline_keyboard=bottons)


def confrim_inline():
    confrim_b = InlineKeyboardButton(text="Да всё верно", callback_data="confrim")
    menu_b = InlineKeyboardButton(text="Меню", callback_data="menu")

    bottons = [[confrim_b], [menu_b]]
    return InlineKeyboardMarkup(inline_keyboard=bottons)

orders_menu_bottons = [[create_order_b, my_orders_b], [cancel_b]]
kb_create_order_bottons = [[confrim_b], [cancel_b]]

kb_orders_menu = ReplyKeyboardMarkup(keyboard=orders_menu_bottons, resize_keyboard=True)
kb_oredr_confrim = ReplyKeyboardMarkup(
    keyboard=kb_create_order_bottons, resize_keyboard=True
)
