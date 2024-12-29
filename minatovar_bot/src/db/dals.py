import asyncio
import json
import aiofiles


from config import DATA_FILE


class DataDAL:
    def __init__(self):
        self.file_lock = asyncio.Lock()

    async def load_data(self) -> dict:
        async with aiofiles.open(DATA_FILE, mode="r") as f:
            data = await f.read()
            return json.loads(data) if data.strip() else {}

    async def save_data(self, data: dict):
        async with self.file_lock:
            async with aiofiles.open(DATA_FILE, mode="w") as f:
                await f.write(json.dumps(data, indent=4, ensure_ascii=False))

    async def get_shoes_price(self):
        delivery_price = await self.load_data()
        if delivery_price := delivery_price.get("shoes_price"):
            return int(delivery_price)

    async def get_cloth_price(self):
        delivery_price = await self.load_data()
        if delivery_price := delivery_price.get("cloth_price"):
            return int(delivery_price)

    async def get_current_rate(self):
        current_rate = await self.load_data()
        if current_rate := current_rate.get("current_rate"):
            return float(current_rate)

    async def set_shoes_price(self, price: int):
        data = await self.load_data()
        data["shoes_price"] = price
        await self.save_data(data)
        return price

    async def set_cloth_price(self, price: int):
        data = await self.load_data()
        data["cloth_price"] = price
        await self.save_data(data)
        return price

    async def set_current_rate(self, rate: float):
        data = await self.load_data()
        data["current_rate"] = rate
        await self.save_data(data)
        return rate
