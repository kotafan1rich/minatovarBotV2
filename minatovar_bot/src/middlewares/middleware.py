from db.session import async_session
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import ReferralDAL, UserDAL
from utils.referral import pars_arg


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        async with async_session() as session:
            data["db_session"] = session
            return await handler(event, data)


class StartMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        if data.get("handler").flags.get("start"):
            message: Message = event
            user_id = message.from_user.id
            username = message.from_user.username
            db_session: AsyncSession = data["db_session"]

            user_dal = UserDAL(db_session)
            referal_dal = ReferralDAL(db_session)
            if not await user_dal.user_exists(user_id):
                await user_dal.add_user(user_id=user_id, username=username)
                arg = pars_arg(message.text)
                referral_id = int(arg) if arg else None
                if referral_id and user_id != referral_id:
                    await referal_dal.add_referal(id_from=referral_id, id_to=user_id)
        return await handler(event, data)


class CallbackDataMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        if isinstance(event, CallbackQuery):
            callback_data = event.data.split("_", maxsplit=1)
            data["calback_key"] = callback_data[0]
            data["calback_arg"] = callback_data[1] if len(callback_data) > 1 else ""
        return await handler(event, data)
