from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F

from db.dals import DataDAL

from .messages import BAD_FORMAT_ERROR, NON_ARGUMENT_ERROR, ADMIN_HELP

from create_bot import bot

admins = [1019030670, 1324716819]

admin_router = Router(name="admin_router")


@admin_router.message(Command("shoes"), F.from_user.id.in_(admins))
async def change_shoes_price(message: types.Message):
    try:
        price = await DataDAL().set_shoes_price(price=int(message.text.split(" ")[1]))

        await bot.send_message(message.from_user.id, str(price))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


@admin_router.message(Command("cloth"), F.from_user.id.in_(admins))
async def change_cloth_price(message: types.Message):
    try:
        price = await DataDAL().set_cloth_price(price=int(message.text.split(" ")[1]))
        await bot.send_message(message.from_user.id, str(price))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


@admin_router(Command("rate"), F.from_user.id.in_(admins))
async def change_current_rate(message: types.Message):
    try:
        rate = await DataDAL().set_current_rate(rate=float(message.text.split(" ")[1]))
        await bot.send_message(message.from_user.id, str(rate))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


@admin_router.message(Command("adminhelp"), F.from_user.id.in_(admins))
async def admin_help(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, ADMIN_HELP)
