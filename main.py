import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from buttons import menuButtons, btn1

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6748283727:AAEkNXsazg5qCLCJkMn6d1um3byKgU98R04"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Assalomu alaykum, {hbold(message.from_user.full_name)}! \nRamazon oyingiz muborak bo'lsin "
                         f"dindoshim!🥳 \n\nBu bot sizga tabrik uchun rasmlar va ramazon taqvimini ko'rsata oladi. "
                         f"\n\nRo'zamiz qabul bo'lsin😊",
                         reply_markup=menuButtons
                         )


@dp.message(F.text == btn1)
async def one_handler(message: types.Message) -> None:
    await message.answer("🎨 Bizda 3 xil dizayn bor, qaysini tanlaysiz?")


@dp.message()
async def not_handler(message: types.Message) -> None:
    await message.answer("🤷‍♂️ Nimadir noto‘g‘ri keti.")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
