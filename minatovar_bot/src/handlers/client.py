from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import STATIC_FILES
from create_bot import bot
from db.dals import ReferralDAL, SettingsDAL
from keyboards import (
    cancel_b,
    main_menu_inline_kb,
    get_menu_inline,
    get_referral_menu_inline,
    get_type_item_inline,
)
from middlewares.middleware import StartMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import OrderTypeItem


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
    await bot.send_message(
        message.from_user.id, START, reply_markup=main_menu_inline_kb()
    )


@client_router.callback_query(F.data.startswith("menu"))
async def get_menu(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text="Что дальше?",
        reply_markup=main_menu_inline_kb(),
    )


@client_router.callback_query(F.data.startswith("help"))
async def help(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(
        call.from_user.id, HELP, reply_markup=main_menu_inline_kb()
    )


@client_router.message(F.text == cancel_b.text)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await message.answer(
        "Отмена",
        reply_markup=main_menu_inline_kb(),
    )


@client_router.callback_query(F.data.startswith("getprice"))
async def get_type(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMGetPrice.get_type_state)
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=TYPE_ITEM,
        reply_markup=get_type_item_inline(),
    )


@client_router.callback_query(FSMGetPrice.get_type_state, F.data.startswith("type_"))
async def set_price_state(
    call: types.CallbackQuery, state: FSMContext, calback_arg: str
):
    if calback_arg == OrderTypeItem.SHOES.value:
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
    await call.answer()
    await bot.send_media_group(call.from_user.id, media=media_group)


@client_router.message(FSMGetPrice.shoes_state)
async def send_shoes_price(message: types.Message, state: FSMContext, db_session):
    user_id = message.from_user.id
    await state.clear()
    price = int(message.text)
    delivery_price = await SettingsDAL(db_session).get_param("shoes_price")
    current_rate = await SettingsDAL(db_session).get_param("current_rate")
    if delivery_price and current_rate:
        result_price = round(price * current_rate + delivery_price, 2)
        text = send_price_mes(result_price)
        await bot.send_message(
            user_id, text
        )
    else:
        await bot.send_message(
            user_id, BOT_IS_UNVAILABLE
        )
    await bot.send_message(user_id, "Главное меню", reply_markup=main_menu_inline_kb())


@client_router.message(FSMGetPrice.cloth_state)
async def send_cloth_price(message: types.Message, state: FSMContext, db_session):
    user_id = message.from_user.id
    await state.clear()
    price = int(message.text)
    delivery_price = await SettingsDAL(db_session).get_param("cloth_price")
    current_rate = await SettingsDAL(db_session).get_param("current_rate")
    if delivery_price and current_rate:
        result_price = round(price * current_rate + delivery_price, 2)

        text = send_price_mes(result_price)
        await bot.send_message(
            user_id, text
        )
    else:
        await bot.send_message(
            user_id, BOT_IS_UNVAILABLE
        )
    await bot.send_message(user_id, "Главное меню", reply_markup=main_menu_inline_kb())



@client_router.callback_query(F.data.startswith("getrate"))
async def get_current_rate(call: types.CallbackQuery, db_session):
    await call.answer()
    if current_rate := await SettingsDAL(db_session).get_param("current_rate"):
        await bot.send_message(
            call.from_user.id,
            send_current_rate_mes(current_rate),
            reply_markup=get_menu_inline(),
        )
    else:
        await bot.send_message(
            call.from_user.id, BOT_IS_UNVAILABLE, reply_markup=main_menu_inline_kb()
        )


@client_router.callback_query(F.data.startswith("referralmenu"))
async def referral_menu(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(
        call.from_user.id, "Что дальше?", reply_markup=get_referral_menu_inline()
    )


@client_router.callback_query(F.data.startswith("referralurl"))
async def get_refferal_link(call: types.CallbackQuery):
    info_bot = await bot.get_me()
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=refferal_link(bot_username=info_bot.username, user_id=call.from_user.id),
        reply_markup=get_menu_inline(),
    )


@client_router.callback_query(F.data.startswith("myreferrals"))
async def get_my_referrals(call: types.CallbackQuery, db_session: AsyncSession):
    referral_dal = ReferralDAL(db_session)
    referrals = await referral_dal.get_refferals(int(call.from_user.id))
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=count_referrals(referrals),
        reply_markup=get_menu_inline(),
    )
