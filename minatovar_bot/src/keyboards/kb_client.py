from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

get_price_b = KeyboardButton(text="Рассчитать стоимость товара")
help_b = KeyboardButton(text="Помощь")
get_cloth_price_b = KeyboardButton(text="Одежда")
get_shoes_price_b = KeyboardButton(text="Обувь")
get_current_rate_b = KeyboardButton(text="Текущий курс юаня")
cancel_b = KeyboardButton(text="Отмена")


kb_client_main_bottons = [[get_price_b, get_current_rate_b], [help_b]]
kb_client_get_price_bottons = [[get_shoes_price_b, get_cloth_price_b], [cancel_b]]
kb_client_cancel_bottons = [[cancel_b]]

kb_client_main = ReplyKeyboardMarkup(
    keyboard=kb_client_main_bottons, resize_keyboard=True
)
kb_client_get_price = ReplyKeyboardMarkup(
    keyboard=kb_client_get_price_bottons, resize_keyboard=True
)
kb_client_cancel = ReplyKeyboardMarkup(
    keyboard=kb_client_cancel_bottons, resize_keyboard=True
)
