from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from .kb_client import cancel_b

create_order_b = KeyboardButton(text="Сделать заказ")
my_orders_b = KeyboardButton(text="Мои заказы")

confrim_b = KeyboardButton(text="Да всё верно")

orders_menu_bottons = [[create_order_b, my_orders_b], [cancel_b]]
kb_create_order_bottons = [[confrim_b], [cancel_b]]

kb_orders_menu = ReplyKeyboardMarkup(keyboard=orders_menu_bottons, resize_keyboard=True)
kb_oredr_confrim = ReplyKeyboardMarkup(
    keyboard=kb_create_order_bottons, resize_keyboard=True
)
