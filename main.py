import asyncio
import logging
import sys
import os
import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from buttons import menuButtons, btn1, btn2, designButtons, regionsButtons, taqvimButtons, back, taqvimButtonToday_text, \
    taqvimButtonTomorrow_text
from states import GiftState
from images import create_image
from models.mics import User, Taqvim
from models.base import db
from context import duo_text
from service import get_taqvim

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
    User.get_or_create(chat_id=message.chat.id)


@dp.message(F.text == btn1, StateFilter(None))
async def one_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer("🎨 Bizda 3 xil dizayn bor, qaysini tanlaysiz?", reply_markup=designButtons)
    await state.set_state(GiftState.design)


@dp.message(F.text == btn2, StateFilter(None))
async def two_handler(message: types.Message) -> None:
    user = User.get_user(message.chat.id)
    if user.region is None:
        await message.answer(f"📅 Taqvimni ko'rish uchun tugmalardan foydalaning.", reply_markup=taqvimButtons)
        return
    await message.answer("📅 Ramazon taqvimini ko'rish uchun joylashuvni tanlang:", reply_markup=regionsButtons())


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


@dp.callback_query(F.data.startswith('region_'))
async def handler(query: CallbackQuery) -> None:
    region = query.data.split('_')[1]
    User.update(region=region).where(User.chat_id == query.message.chat.id).execute()
    await query.message.answer("Joylashuv qabul qilindi. Taqvimni ko'rish uchun tugmalardan foydalaning.",
                               reply_markup=taqvimButtons)
    await query.message.delete()


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
    await message.answer_photo(photo=photo,
                               caption=f"🎉 Tabrik noma tayyor! \n\n👤 Ism: {data['name']} \n👥 Tabrik noma beruvchi: {message.text}",
                               reply_markup=menuButtons)

    await loader_message.delete()
    await state.clear()
    os.remove(f"{data['name']}.jpg")


@dp.message(F.text == taqvimButtonToday_text, StateFilter(None))
async def taqvim_handler(message: types.Message) -> None:
    user = User.get_user(message.chat.id)
    if not user.region:
        await message.answer("🤷‍♂️ Sizda joylashuvni tanlamaganmisiz? Qaytadan tanlang:", reply_markup=regionsButtons())
        return
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    taqvim = Taqvim.get_or_none((Taqvim.region.contains(user.region)) & (Taqvim.date == date))
    if not taqvim:
        await message.answer("📅 Taqvim hozircha mavjud emas.")
        return
    photo = types.FSInputFile(f"images/{user.region}/{taqvim.img}")
    await message.answer_photo(photo=photo, caption=duo_text, reply_markup=menuButtons)


@dp.message(F.text == taqvimButtonTomorrow_text, StateFilter(None))
async def taqvim_handler(message: types.Message) -> None:
    user = User.get_user(message.chat.id)
    if not user.region:
        await message.answer("🤷‍♂️ Sizda joylashuvni tanlamaganmisiz? Qaytadan tanlang:", reply_markup=regionsButtons())
        return
    date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    taqvim = Taqvim.get_taqvim(user.region, date)
    if not taqvim:
        await message.answer("📅 Taqvim hozircha mavjud emas.")
        return
    photo = types.FSInputFile(f"images/{user.region}/{taqvim.img}")
    await message.answer_photo(photo=photo, caption=duo_text, reply_markup=menuButtons)


@dp.message(F.text == back, StateFilter(None))
async def back_handler(message: types.Message) -> None:
    await message.answer("🏘 Asosiy menyuga qaytib keldik.", reply_markup=menuButtons)


@dp.message()
async def not_handler(message: types.Message) -> None:
    await message.answer("🤷‍♂️ Nimadir noto‘g‘ri keti.")


async def main() -> None:
    db.connect()
    db.create_tables([User, Taqvim])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
