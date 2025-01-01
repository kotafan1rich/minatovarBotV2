import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import (
    main_admin_kb,
    all_active_orders_b,
    all_completed_orders_b,
    get_info_order_inline,
    get_status_order_inline,
)
from db.dals import OrderDAL, SettingsDAL, UserDAL
from db.models import OrderStatus

from .messages import (
    BAD_FORMAT_ERROR,
    NON_ARGUMENT_ERROR,
    ADMIN_HELP,
    get_order,
    get_order_for_admin,
)

from create_bot import bot

admins = [1019030670, 1324716819]

admin_router = Router(name="admin_router")


@admin_router.message(Command("admin"), F.from_user.id.in_(admins))
async def admin(message: types.Message):
    await bot.send_message(
        message.from_user.id, "Отпарвьте команду", reply_markup=main_admin_kb
    )


@admin_router.message(
    F.text.in_([all_active_orders_b.text, all_completed_orders_b.text]),
    F.from_user.id.in_(admins),
)
async def get_orders(message: types.Message, db_session: AsyncSession):
    user_id = message.from_user.id
    order_dal = OrderDAL(db_session)
    user_dal = UserDAL(db_session)
    user = await user_dal.get_user(user_id)
    username = user.username
    if message.text == all_active_orders_b.text:
        orders = await order_dal.get_all_active_orders()
    else:
        orders = await order_dal.get_completed_orders()
    if orders:
        for order in orders:
            await bot.send_message(
                user_id,
                get_order_for_admin(order, username),
                reply_markup=get_info_order_inline(order.id),
            )
    else:
        await bot.send_message(user_id, "Нет заказов")


@admin_router.callback_query(F.data.startswith("status_"))
async def get_order_status(call: types.CallbackQuery, calback_arg: str):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=get_status_order_inline(int(calback_arg)),
    )


@admin_router.callback_query(F.data.startswith("chstatus_"))
async def change_order_status(
    call: types.CallbackQuery, calback_arg: str, db_session: AsyncSession
):
    user_id = call.from_user.id
    split_arg = calback_arg.split("_")
    status = split_arg[0]
    order_id = int(split_arg[1])
    order_dal = OrderDAL(db_session)
    status_enum = next((s for s in OrderStatus if s.value == status), None)

    if status_enum is None:
        raise ValueError(f"Invalid status: {status}")
    changed_order = await order_dal.update_order(id=order_id, status=status_enum)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=get_order(changed_order),
        reply_markup=get_info_order_inline(changed_order.id),
    )


@admin_router.callback_query(F.data.startswith("remove_"))
async def remove_order(
    call: types.CallbackQuery, calback_arg: str, db_session: AsyncSession
):
    order_dal = OrderDAL(db_session)
    await order_dal.delete_order(int(calback_arg))
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@admin_router.callback_query(F.data.startswith("backorder_"))
async def back_order(call: types.CallbackQuery, calback_arg: str):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=get_info_order_inline(int(calback_arg)),
    )


@admin_router.message(Command("shoes"), F.from_user.id.in_(admins))
async def change_shoes_price(message: types.Message, db_session: AsyncSession):
    try:
        price = await SettingsDAL(db_session).update_param(
            key="shoes_price", value=float(message.text.split(" ")[1])
        )

        await bot.send_message(message.from_user.id, str(price))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


@admin_router.message(Command("cloth"), F.from_user.id.in_(admins))
async def change_cloth_price(message: types.Message, db_session: AsyncSession):
    try:
        price = await SettingsDAL(db_session).update_param(
            key="cloth_price", value=float(message.text.split(" ")[1])
        )
        await bot.send_message(message.from_user.id, str(price))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


@admin_router.message(Command("rate"), F.from_user.id.in_(admins))
async def change_current_rate(message: types.Message, db_session: AsyncSession):
    try:
        rate = await SettingsDAL(db_session).update_param(
            key="current_rate", value=float(message.text.split(" ")[1])
        )
        await bot.send_message(message.from_user.id, str(rate))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


@admin_router.message(Command("adminhelp"), F.from_user.id.in_(admins))
async def admin_help(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, ADMIN_HELP)
