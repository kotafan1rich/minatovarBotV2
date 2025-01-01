from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from create_bot import bot
from db.dals import OrderDAL, UserDAL
from db.models import Order, OrderTypeItem
from keyboards import (
    confrim_b,
    get_cloth_b,
    get_shoes_b,
    kb_client_cancel,
    kb_client_get_type,
    kb_client_main,
    kb_oredr_confrim,
    create_order_b,
    order_b,
    kb_orders_menu,
    my_orders_b
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils.orders import calculate_rub_price, is_valid_link

from handlers.messages import confrim_order, get_order

order_roter = Router(name="order_handler")


class FSMOrder(StatesGroup):
    url = State()
    type_item = State()
    addres = State()
    price_cny = State()
    size = State()
    confrim = State()


@order_roter.message(F.text == order_b.text)
async def order_menu(message: types.Message):
    await bot.send_message(
        message.from_user.id, "Что дальше?", reply_markup=kb_orders_menu
    )


@order_roter.message(F.text == my_orders_b.text)
async def get_my_orders(message: types.Message, db_session: AsyncSession):
    user_id = message.from_user.id
    order_dal = OrderDAL(db_session)
    orders = await order_dal.get_orders_for_user(user_id)
    if orders:
        for order in orders:
            await bot.send_message(user_id, get_order(order))
    else:
        await bot.send_message(user_id, "У вас нет заказов")


@order_roter.message(F.text == create_order_b.text)
async def create_order(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.from_user.username:
        await bot.send_message(
            user_id, "Отпрвьте url товара", reply_markup=kb_client_cancel
        )
        await state.set_state(FSMOrder.url)
    else:
        await bot.send_message(
            user_id,
            "Установите username и повторите попытку",
            reply_markup=kb_client_main,
        )


@order_roter.message(FSMOrder.url)
async def get_url(messgae: types.Message, state: FSMContext):
    url = messgae.text
    user_id = messgae.from_user.id
    if is_valid_link(url):
        await state.update_data(url=url)
        await bot.send_message(
            user_id, "Укажите тип товара", reply_markup=kb_client_get_type
        )
        await state.set_state(FSMOrder.type_item)
    else:
        await bot.send_message(
            user_id, "Некорректная ссылка", reply_markup=kb_client_cancel
        )


@order_roter.message(
    FSMOrder.type_item, F.text.in_([get_shoes_b.text, get_cloth_b.text])
)
async def get_type_item(messgae: types.Message, state: FSMContext):
    await state.update_data(type_item=messgae.text)
    await state.set_state(FSMOrder.addres)
    await bot.send_message(
        messgae.from_user.id, "Отправьте адрес", reply_markup=kb_client_cancel
    )


@order_roter.message(FSMOrder.addres)
async def get_addres(messgae: types.Message, state: FSMContext):
    addres = messgae.text
    await state.update_data(addres=addres)
    await bot.send_message(
        messgae.from_user.id, "Отправьте цену", reply_markup=kb_client_cancel
    )
    await state.set_state(FSMOrder.price_cny)


@order_roter.message(FSMOrder.price_cny)
async def get_prcie(messgae: types.Message, state: FSMContext):
    price = int(messgae.text)
    await state.update_data(price_cny=price)
    await bot.send_message(
        messgae.from_user.id, "Отправьте размер", reply_markup=kb_client_cancel
    )
    await state.set_state(FSMOrder.size)


@order_roter.message(FSMOrder.size)
async def get_size(messgae: types.Message, state: FSMContext, db_session: AsyncSession):
    user_id = messgae.from_user.id
    size = messgae.text.replace(",", ".")
    size = float(size)
    await state.update_data(size=size)
    data = await state.get_data()
    res_price_rub = await calculate_rub_price(
        user_id=user_id,
        price_cny=data["price_cny"],
        type_item=data["type_item"],
        db_session=db_session,
    )

    data["price_rub"] = res_price_rub
    await state.set_data(data)
    order = confrim_order(Order(**data))
    await bot.send_message(user_id, order, reply_markup=kb_oredr_confrim)
    await state.set_state(FSMOrder.confrim)


@order_roter.message(FSMOrder.confrim, F.text == confrim_b.text)
async def confrim(messgae: types.Message, state: FSMContext, db_session: AsyncSession):
    user_id = messgae.from_user.id
    user_dal = UserDAL(db_session)
    order_dal = OrderDAL(db_session)
    data = await state.get_data()
    if data["type_item"] == get_shoes_b.text:
        data["type_item"] = OrderTypeItem.SHOES
    else:
        data["type_item"] = OrderTypeItem.CLOTH
    await user_dal.update_user(user_id=user_id, username=messgae.from_user.username)
    created_order = await order_dal.add_order(user_id=user_id, **data)
    res = get_order(created_order)

    await bot.send_message(
        user_id,
        res,
        reply_markup=kb_client_main,
    )
    await state.clear()
