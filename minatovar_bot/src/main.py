#!/usr/bin/python
# vim: set fileencoding=UTF-8
import asyncio
import logging
from aiogram.types import BotCommand
from create_bot import bot, dp
from handlers import client, admin, orders
from db.dals import SettingsDAL
from db.session import async_session
from middlewares.middleware import (
    DBSessionMiddleware,
    StartMiddleware,
    CallbackDataMiddleware,
)

logging.basicConfig(level=logging.INFO)


async def on_startapp():
    await bot.set_my_commands([BotCommand(command="/start", description="Начать")])
    async with async_session() as session:
        settings_dal = SettingsDAL(session)
        if not await settings_dal.param_exists("current_rate"):
            await settings_dal.set_param("current_rate", 0.0)
        if not await settings_dal.param_exists("shoes_price"):
            await settings_dal.set_param("shoes_price", 0.0)
        if not await settings_dal.param_exists("cloth_price"):
            await settings_dal.set_param("cloth_price", 0.0)


async def main():
    await dp.emit_startup(await on_startapp())
    await bot.delete_webhook()
    dp.update.outer_middleware(DBSessionMiddleware())
    admin.admin_router.callback_query.middleware(CallbackDataMiddleware())
    client.client_router.message.middleware(StartMiddleware())
    dp.include_router(client.client_router)
    dp.include_router(orders.order_roter)
    dp.include_router(admin.admin_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
