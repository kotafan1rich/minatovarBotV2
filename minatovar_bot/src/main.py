#!/usr/bin/python
# vim: set fileencoding=UTF-8
import asyncio
import logging
import os

from config import DATA_FILE
from create_bot import bot, dp
from handlers import client, admin
from db.dals import DataDAL

logging.basicConfig(level=logging.INFO)

client.register_handlers_client(dp)

dp.include_router(admin.admin_router)


async def on_startapp():
    default_data = {"current_rate": None, "cloth_price": None, "shoes_price": None}
    if not os.path.exists(DATA_FILE):
        await DataDAL().save_data(default_data)
    else:
        data = await DataDAL().load_data()
        if not data:
            DataDAL().save_data(default_data)


async def main():
    await on_startapp()
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
