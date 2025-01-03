#!/usr/bin/python
# vim: set fileencoding=UTF-8
import asyncio
from aiogram.types import BotCommand
from create_bot import bot, dp
from db.dals import SettingsDAL
from handlers import admin_router, client_router, order_roter
from db.session import async_session
from middlewares.middleware import (
    DBSessionMiddleware,
    StartMiddleware,
    CallbackDataMiddleware,
)


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
    admin_router.callback_query.middleware.register(CallbackDataMiddleware())
    order_roter.callback_query.middleware.register(CallbackDataMiddleware())
    client_router.message.middleware.register(StartMiddleware())
    client_router.callback_query.middleware.register(CallbackDataMiddleware())
    dp.include_router(client_router)
    dp.include_router(order_roter)
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
