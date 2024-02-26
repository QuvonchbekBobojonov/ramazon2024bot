import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from buttons import menuButtons, btn1, btn2, designButtons
from states import GiftState
from images import create_image

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6748283727:AAEkNXsazg5qCLCJkMn6d1um3byKgU98R04"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Assalomu alaykum, {hbold(message.from_user.full_name)}! \nRamazon oyingiz muborak bo'lsin "
                         f"dindoshim!🥳 \n\nBu bot sizga tabrik uchun rasmlar va ramazon taqvimini ko'rsata oladi. "
                         f"\n\nRo'zamiz qabul bo'lsin😊",
                         reply_markup=menuButtons)


@dp.message(F.text == btn1, StateFilter(None))
async def one_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer("🎨 Bizda 3 xil dizayn bor, qaysini tanlaysiz?", reply_markup=designButtons)
    await state.set_state(GiftState.design)


@dp.callback_query(F.data.startswith('design_'), GiftState.design)
async def handler(query: CallbackQuery, state: FSMContext) -> None:
    if query.data == "design_back":
        await query.message.delete()
        await query.message.answer("🏘 Asosiy menyuga qaytib keldik.", reply_markup=menuButtons)
        await state.clear()
        return
    await state.update_data(design=query.data)
    await query.message.answer("📝 Tabrik noma uchun ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(GiftState.name)


@dp.message(GiftState.name, F.text)
async def handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("📝 Tabrik noma beruvchining ismini kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(GiftState.author)


@dp.message(GiftState.author, F.text)
async def handler(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    loader_message = await message.answer("🎁 Tabrik noma tayyorlanmoqda, iltimos kuting...")
    create_image(data['name'], message.text, data['design'])
    photo = types.FSInputFile(f"{data['name']}.jpg")
    await message.answer_photo(photo=photo, caption=f"🎉 Tabrik noma tayyor! \n\n👤 Ism: {data['name']} \n👥 Tabrik noma beruvchi: {message.text}",
                               reply_markup=menuButtons)

    await loader_message.delete()
    await state.clear()
    os.remove(f"{data['name']}.jpg")


@dp.message()
async def not_handler(message: types.Message) -> None:
    await message.answer("🤷‍♂️ Nimadir noto‘g‘ri keti.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
