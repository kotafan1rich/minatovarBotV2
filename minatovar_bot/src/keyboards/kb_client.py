from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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
