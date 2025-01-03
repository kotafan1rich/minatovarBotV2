from typing import Union

from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Order, OrderStatus, Referral, Settings, User


class BaseDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


class SettingsDAL(BaseDAL):
    async def param_exists(self, key: str) -> bool:
        query = select(exists().where(Settings.key == key))
        res = await self.db_session.execute(query)
        return res.scalar()

    async def update_param(self, key: str, value: float):
        query = (
            update(Settings)
            .where(Settings.key == key)
            .values(value=value)
            .returning(Settings.value)
        )
        res = await self.db_session.execute(query)
        await self.db_session.commit()
        return res.scalar_one_or_none()

    async def set_param(self, key: str, value: float):
        new_param = Settings(key=key, value=value)
        self.db_session.add(new_param)
        await self.db_session.commit()
        return value

    async def get_param(self, key: str):
        query = select(Settings.value).where(Settings.key == key)
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()


class UserDAL(BaseDAL):
    async def add_user(self, user_id: int, username: str = None):
        new_user = User(user_id=user_id, username=username)
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user

    async def update_user(self, user_id: int, **kwargs):
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        await self.db_session.commit()
        return res.scalar_one_or_none()

    async def user_exists(self, user_id: int) -> bool:
        query = select(exists().where(User.user_id == user_id))
        res = await self.db_session.execute(query)
        return res.scalar()

    async def get_user(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        return res.scalar()


class ReferralDAL(BaseDAL):
    async def add_referal(self, id_from: int, id_to: int):
        new_referral = Referral(id_from=id_from, id_to=id_to)
        self.db_session.add(new_referral)
        await self.db_session.commit()
        return new_referral

    async def referral_exists(self, id_to: int):
        query = select(exists().where(Referral.id_to == id_to))
        res = await self.db_session.execute(query)
        return res.scalar()

    async def get_refferals(self, id_from: int):
        query = select(Referral.id_to).where(Referral.id_from == id_from)
        res = await self.db_session.execute(query)
        return res.scalars().all()


class OrderDAL(BaseDAL):
    async def add_order(self, user_id: int, **kwargs) -> Union[Order, None]:
        order = Order(user_id=user_id, **kwargs)
        self.db_session.add(order)
        await self.db_session.commit()
        return order

    async def get_completed_orders_for_user(self, user_id: int):
        query = (
            select(Order.price_rub)
            .where(Order.status == OrderStatus.COMPLETED, Order.user_id == user_id)
            .order_by(Order.id)
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_orders_for_user(self, user_id: int):
        query = select(Order).where(Order.user_id == user_id).order_by(Order.id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_completed_orders(self):
        query = (
            select(Order)
            .where(Order.status == OrderStatus.COMPLETED)
            .order_by(Order.id)
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_all_active_orders(self):
        query = (
            select(Order)
            .where(Order.status != OrderStatus.COMPLETED)
            .order_by(Order.id)
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def update_order(self, id: int, **kwargs):
        query = update(Order).where(Order.id == id).values(kwargs).returning(Order)
        res = await self.db_session.execute(query)
        await self.db_session.commit()
        return res.scalar_one_or_none()

    async def delete_order(self, id: int):
        query = delete(Order).where(Order.id == id)
        await self.db_session.execute(query)
        await self.db_session.commit()
        return id
