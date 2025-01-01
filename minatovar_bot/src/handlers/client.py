from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import STATIC_FILES
from create_bot import bot
from db.dals import ReferralDAL, SettingsDAL
from keyboards import (
    cancel_b,
    get_cloth_b,
    get_current_rate_b,
    get_price_b,
    get_shoes_b,
    help_b,
    kb_client_get_type,
    kb_client_main,
    my_referrals_b,
    referral_b,
    referral_menu_b,
    kb_client_referral_menu,
)
from middlewares.middleware import StartMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from .messages import (
    BOT_IS_UNVAILABLE,
    HELP,
    SEND_PRICE,
    START,
    TYPE_ITEM,
    count_referrals,
    refferal_link,
    send_current_rate_mes,
    send_price_mes,
)

client_router = Router(name="client_router")
start_middleware = StartMiddleware()


class FSMGetPrice(StatesGroup):
    get_type_state = State()
    shoes_state = State()
    cloth_state = State()


@client_router.message(Command("start"), flags={"start": True})
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, START, reply_markup=kb_client_main)


@client_router.message(F.text == help_b.text)
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, HELP, reply_markup=kb_client_main)


@client_router.message(F.text == cancel_b.text)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await message.answer(
        "Отмена",
        reply_markup=kb_client_main,
    )


@client_router.message(F.text == get_price_b.text)
async def get_type(message: types.Message, state: FSMContext):
    await state.set_state(FSMGetPrice.get_type_state)
    await bot.send_message(
        message.from_user.id, TYPE_ITEM, reply_markup=kb_client_get_type
    )


@client_router.message(
    FSMGetPrice.get_type_state,
    F.text.in_((get_shoes_b.text, get_cloth_b.text)),
)
async def set_price_state(message: types.Message, state: FSMContext):
    if message.text == get_shoes_b.text:
        media_group = [
            types.InputMediaPhoto(
                media=types.FSInputFile(f"{STATIC_FILES}/shoes_price_2.jpg")
            ),
            types.InputMediaPhoto(
                media=types.FSInputFile(f"{STATIC_FILES}/shoes_price.jpg"),
                caption=SEND_PRICE,
            ),
        ]
        await state.set_state(FSMGetPrice.shoes_state)
    else:
        media_group = [
            types.InputMediaPhoto(
                media=types.FSInputFile(f"{STATIC_FILES}/cloth_price_2.jpg")
            ),
            types.InputMediaPhoto(
                media=types.FSInputFile(f"{STATIC_FILES}/cloth_price.jpg"),
                caption=SEND_PRICE,
            ),
        ]
        await state.set_state(FSMGetPrice.cloth_state)
    await bot.send_media_group(message.from_user.id, media=media_group)


@client_router.message(FSMGetPrice.shoes_state)
async def send_shoes_price(message: types.Message, state: FSMContext, db_session):
    await state.clear()
    price = int(message.text)
    delivery_price = await SettingsDAL(db_session).get_param("shoes_price")
    current_rate = await SettingsDAL(db_session).get_param("current_rate")
    if delivery_price and current_rate:
        result_price = round(price * current_rate + delivery_price, 2)

        text = send_price_mes(result_price)
        await bot.send_message(message.from_user.id, text, reply_markup=kb_client_main)
    else:
        await bot.send_message(
            message.from_user.id, BOT_IS_UNVAILABLE, reply_markup=kb_client_main
        )


@client_router.message(FSMGetPrice.cloth_state)
async def send_cloth_price(message: types.Message, state: FSMContext, db_session):
    await state.clear()
    price = int(message.text)
    delivery_price = await SettingsDAL(db_session).get_param("cloth_price")
    current_rate = await SettingsDAL(db_session).get_param("current_rate")
    if delivery_price and current_rate:
        result_price = round(price * current_rate + delivery_price, 2)

        text = send_price_mes(result_price)
        await bot.send_message(message.from_user.id, text, reply_markup=kb_client_main)
    else:
        await bot.send_message(
            message.from_user.id, BOT_IS_UNVAILABLE, reply_markup=kb_client_main
        )


@client_router.message(F.text == get_current_rate_b.text)
async def get_current_rate(message: types.Message, db_session):
    if current_rate := await SettingsDAL(db_session).get_param("current_rate"):
        await bot.send_message(
            message.from_user.id,
            send_current_rate_mes(current_rate),
            reply_markup=kb_client_main,
        )
    else:
        await bot.send_message(
            message.from_user.id, BOT_IS_UNVAILABLE, reply_markup=kb_client_main
        )


@client_router.message(F.text == referral_menu_b.text)
async def referral_menu(message: types.Message):
    await bot.send_message(
        message.from_user.id, "Что дальше?", reply_markup=kb_client_referral_menu
    )


@client_router.message(F.text == referral_b.text)
async def get_refferal_link(message: types.Message):
    info_bot = await bot.get_me()
    await bot.send_message(
        message.from_user.id,
        refferal_link(bot_username=info_bot.username, user_id=message.from_user.id),
        reply_markup=kb_client_main,
    )


@client_router.message(F.text == my_referrals_b.text)
async def get_my_referrals(message: types.Message, db_session: AsyncSession):
    referral_dal = ReferralDAL(db_session)
    referrals = await referral_dal.get_refferals(int(message.from_user.id))
    await bot.send_message(
        message.from_user.id, count_referrals(referrals), reply_markup=kb_client_main
    )
