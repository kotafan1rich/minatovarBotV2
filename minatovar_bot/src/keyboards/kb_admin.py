from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from db.models import OrderStatus

from .kb_client import cancel_b

all_active_orders_b = KeyboardButton(text="Активные заказы")
all_completed_orders_b = KeyboardButton(text="Завершенные заказы")

main_admin_kb_bottons = [[all_active_orders_b, all_completed_orders_b], [cancel_b]]
main_admin_kb = ReplyKeyboardMarkup(
    keyboard=main_admin_kb_bottons, resize_keyboard=True
)


def get_info_order_inline(id: int):
    change_status_b = InlineKeyboardButton(
        text="Изменить статус", callback_data=f"status_{id}"
    )
    remove_b = InlineKeyboardButton(text="Удалить заказ", callback_data=f"remove_{id}")

    bottons = [[change_status_b], [remove_b]]
    return InlineKeyboardMarkup(inline_keyboard=bottons)


def get_status_order_inline(id: int):
    bottons = [
        [
            InlineKeyboardButton(
                text=f"{status.value}", callback_data=f"chstatus_{status.value}_{id}"
            )
        ]
        for status in OrderStatus
    ]
    bottons.append(
        [InlineKeyboardButton(text="Назад", callback_data=f"backorder_{id}")]
    )
    return InlineKeyboardMarkup(inline_keyboard=bottons)
