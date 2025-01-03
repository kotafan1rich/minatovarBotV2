from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from db.models import OrderTypeItem

get_price_b = KeyboardButton(text="Рассчитать стоимость товара")
help_b = KeyboardButton(text="Помощь")
get_cloth_b = KeyboardButton(text="Одежда")
get_shoes_b = KeyboardButton(text="Обувь")
get_current_rate_b = KeyboardButton(text="Текущий курс юаня")
order_b = KeyboardButton(text="Заказы")
referral_menu_b = KeyboardButton(text="Рефералы")
referral_b = KeyboardButton(text="Моя ссылка")
my_referrals_b = KeyboardButton(text="Мои рефералы")
cancel_b = KeyboardButton(text="Отмена")


def main_menu_inline_kb():
    get_price_b = InlineKeyboardButton(
        text="Рассчитать стоимость товара", callback_data="getprice"
    )
    get_current_rate_b = InlineKeyboardButton(
        text="Текущий курс юаня", callback_data="getrate"
    )
    order_b = InlineKeyboardButton(text="Заказы", callback_data="orders")
    referral_menu_b = InlineKeyboardButton(
        text="Рефералы", callback_data="referralmenu"
    )
    help_b = InlineKeyboardButton(text="Помощь", callback_data="help")
    kb_client_main_inline_bottons = [
        [get_price_b],
        [get_current_rate_b],
        [order_b, referral_menu_b],
        [help_b],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_client_main_inline_bottons)


def get_menu_inline():
    menu_b = InlineKeyboardButton(text="Меню", callback_data="menu")
    return InlineKeyboardMarkup(inline_keyboard=[[menu_b]])


def get_referral_menu_inline():
    my_referrals_b = InlineKeyboardButton(
        text="Мои рефералы", callback_data="myreferrals"
    )
    referral_b = InlineKeyboardButton(text="Моя ссылка", callback_data="referralurl")
    menu_b = InlineKeyboardButton(text="Меню", callback_data="menu")

    bottons = [[referral_b, my_referrals_b], [menu_b]]
    return InlineKeyboardMarkup(inline_keyboard=bottons)


def get_type_item_inline():
    get_cloth_b = InlineKeyboardButton(
        text=OrderTypeItem.CLOTH.value,
        callback_data=f"type_{OrderTypeItem.CLOTH.value}",
    )
    get_shoes_b = InlineKeyboardButton(
        text=OrderTypeItem.SHOES.value,
        callback_data=f"type_{OrderTypeItem.SHOES.value}",
    )
    menu_b = InlineKeyboardButton(text="Меню", callback_data="menu")

    bottons = [[get_shoes_b, get_cloth_b], [menu_b]]
    return InlineKeyboardMarkup(inline_keyboard=bottons)


kb_client_main_bottons = [
    [get_price_b, get_current_rate_b],
    [order_b, referral_menu_b],
    [help_b],
]
kb_client_get_type_bottons = [[get_shoes_b, get_cloth_b], [cancel_b]]
kb_client_cancel_bottons = [[cancel_b]]
kb_client_referral_menu_botons = [[referral_b, my_referrals_b], [cancel_b]]

kb_client_main = ReplyKeyboardMarkup(
    keyboard=kb_client_main_bottons, resize_keyboard=True
)
kb_client_get_type = ReplyKeyboardMarkup(
    keyboard=kb_client_get_type_bottons, resize_keyboard=True
)
kb_client_referral_menu = ReplyKeyboardMarkup(
    keyboard=kb_client_referral_menu_botons, resize_keyboard=True
)
kb_client_cancel = ReplyKeyboardMarkup(
    keyboard=kb_client_cancel_bottons, resize_keyboard=True
)
