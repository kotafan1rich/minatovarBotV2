import logging
import re

from db.dals import OrderDAL, ReferralDAL, SettingsDAL
from db.models import OrderTypeItem


def is_valid_link(link: str) -> bool:
    pattern = r"^https://dw4\.co/t/A/[a-zA-Z0-9]+$"
    return bool(re.match(pattern, link))


async def calculate_rub_price(
    user_id: int, price_cny: int, type_item: OrderTypeItem, db_session
):
    referral_dal = ReferralDAL(db_session)
    order_dal = OrderDAL(db_session)
    settings_dal = SettingsDAL(db_session)
    current_rate: float = await settings_dal.get_param("current_rate")
    deliver_price = (
        await settings_dal.get_param("shoes_price")
        if type_item == OrderTypeItem.SHOES.value
        else await settings_dal.get_param("cloth_price")
    )
    user_referrals: list = await referral_dal.get_refferals(id_from=user_id)
    k = 0
    for id_ref in user_referrals:
        summ = sum(await order_dal.get_completed_orders_for_user(user_id=id_ref))
        if summ >= 4000:
            k += 1
    price_rub = price_cny * current_rate + deliver_price
    if k:
        if price_rub < 10000:
            k = min(k, 5)
            price_rub *= (1 - k * 0.1)
        elif price_rub < 20000:
            k = min(k, 3)
            price_rub *= (1 - k * 0.1)
        else:
            k = min(k, 4)
            price_rub *= 1 - k * 0.05
    return round(price_rub)
