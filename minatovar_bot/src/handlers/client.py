from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from db.dals import DataDAL

from keyboards import (
    cancel_b,
    get_price_b,
    get_shoes_price_b,
    kb_client_main,
    kb_client_get_price,
    help_b,
    get_current_rate_b,
    get_cloth_price_b,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .messages import (
    SEND_PRICE,
    START,
    HELP,
    TYPE_ITEM,
    BOT_IS_UNVAILABLE,
    send_current_rate_mes,
    send_price_mes,
)

from config import STATIC_FILES

from create_bot import bot

client_router = Router(name="client_router")


class FSMGetPrice(StatesGroup):
    get_type_state = State()
    shoes_state = State()
    cloth_state = State()


async def start(message: types.Message):
    await bot.send_message(message.from_user.id, START, reply_markup=kb_client_main)


async def help(message: types.Message):
    await bot.send_message(message.from_user.id, HELP, reply_markup=kb_client_main)


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await message.answer(
        "Отмена",
        reply_markup=kb_client_main,
    )


async def get_type(message: types.Message, state: FSMContext):
    await state.set_state(FSMGetPrice.get_type_state)
    await bot.send_message(
        message.from_user.id, TYPE_ITEM, reply_markup=kb_client_get_price
    )


async def set_price_state(message: types.Message, state: FSMContext):
    if message.text == get_shoes_price_b.text:
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


async def send_shoes_price(message: types.Message, state: FSMContext):
    await state.clear()
    price = int(message.text)
    delivery_price = await DataDAL().get_shoes_price()
    current_rate = await DataDAL().get_current_rate()
    if delivery_price and current_rate:
        result_price = round(price * current_rate + delivery_price, 2)

        text = send_price_mes(result_price)
        await bot.send_message(message.from_user.id, text, reply_markup=kb_client_main)
    else:
        await bot.send_message(
            message.from_user.id, BOT_IS_UNVAILABLE, reply_markup=kb_client_main
        )


async def send_cloth_price(message: types.Message, state: FSMContext):
    await state.clear()
    price = int(message.text)
    delivery_price = await DataDAL().get_cloth_price()
    current_rate = await DataDAL().get_current_rate()
    if delivery_price and current_rate:
        result_price = round(price * current_rate + delivery_price, 2)

        text = send_price_mes(result_price)
        await bot.send_message(message.from_user.id, text, reply_markup=kb_client_main)
    else:
        await bot.send_message(
            message.from_user.id, BOT_IS_UNVAILABLE, reply_markup=kb_client_main
        )


async def get_current_rate(message: types.Message):
    if current_rate := await DataDAL().get_current_rate():
        await bot.send_message(
            message.from_user.id,
            send_current_rate_mes(current_rate),
            reply_markup=kb_client_main,
        )
    else:
        await bot.send_message(
            message.from_user.id, BOT_IS_UNVAILABLE, reply_markup=kb_client_main
        )


def register_handlers_client(dp: Dispatcher):
    dp.message.register(start, Command("start"))
    dp.message.register(help, F.text == help_b.text)
    dp.message.register(cancel_handler, F.text == cancel_b.text)
    dp.message.register(get_type, F.text == get_price_b.text)
    dp.message.register(get_current_rate, F.text == get_current_rate_b.text)
    dp.message.register(
        set_price_state,
        FSMGetPrice.get_type_state,
        F.text.in_((get_shoes_price_b.text, get_cloth_price_b.text)),
    )
    dp.message.register(send_shoes_price, FSMGetPrice.shoes_state)
    dp.message.register(send_cloth_price, FSMGetPrice.cloth_state)
