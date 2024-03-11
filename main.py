import asyncio
import logging
import sys
import os
import datetime
import requests

from aiogram.utils.chat_action import ChatActionSender

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

import states
from buttons import menuButtons, btn1, btn2, designButtons, regionsButtons, taqvimButtons, back, taqvimButtonToday_text, \
    taqvimButtonTomorrow_text, channelsButtons
from states import GiftState
from images import create_image
from models.mics import User, Taqvim
from models.base import db
from context import duo_text
from filters import ChatTypeFilter

import config
from utils import is_channel

dp = Dispatcher()
bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Assalomu alaykum, {hbold(message.from_user.full_name)}! \nRamazon oyingiz muborak bo'lsin "
                         f"dindoshim!🥳 \n\nBu bot sizga tabrik uchun rasmlar va ramazon taqvimini ko'rsata oladi. "
                         f"\n\nRo'zamiz qabul bo'lsin😊",
                         reply_markup=menuButtons)
    User.get_or_create(chat_id=message.chat.id)


@dp.message(F.text == btn1, StateFilter(None))
async def one_handler(message: types.Message, state: FSMContext) -> None:
    is_ch = await is_channel(bot, message.from_user.id, config.CHANNELS)
    if not is_ch:
        await message.answer("❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak.",
                             reply_markup=channelsButtons())
        return
    await message.answer("🎨 Bizda 3 xil dizayn bor, qaysini tanlaysiz?", reply_markup=designButtons)
    await state.set_state(GiftState.design)


@dp.message(F.text == btn2, StateFilter(None))
async def two_handler(message: types.Message, state: FSMContext) -> None:
    is_ch = await is_channel(bot, message.from_user.id, config.CHANNELS)
    if not is_ch:
        await message.answer("❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak.",
                             reply_markup=channelsButtons())
        return
    await message.answer("📅 Ramazon taqvimini ko'rish uchun manzilingizni yozing:")
    await state.set_state(states.OneState.first)


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


@dp.callback_query(F.data == 'confirm')
async def inline_query_handler(query: types.CallbackQuery):
    is_ch = await is_channel(bot, query.from_user.id, config.CHANNELS)
    if is_ch:
        await query.message.delete()
        await query.message.answer("🏘 Asosiy menyuga qaytib keldik.", reply_markup=menuButtons)
    else:
        await query.answer("❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak.",
                           show_alert=True)


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


@dp.message(F.text, states.OneState.first)
async def taqvim_handler(message: types.Message, state: FSMContext) -> None:
    response = requests.get(f"https://islomapi.uz/api/present/day?region={message.text}")
    data = response.json()
    status = response.status_code
    if status == 404:
        await message.answer("🤷‍♂️ Bunday joylashuv mavjud emas. Qaytadan urinib ko'ring.")
        return
    if status != 200:
        await message.answer("🤷‍♂️ Nimadir noto‘g‘ri keti.")
        return
    try:
        tong_saharlik = datetime.datetime.strptime(data['times']['tong_saharlik'], "%H:%M")
        shom_iftor = datetime.datetime.strptime(data['times']['shom_iftor'], "%H:%M")
        await message.answer(
            f"Mintaqa: {data['region']} \nSahar va Iftar vaqtlari: \n\n🌙 Sahar: {tong_saharlik.time()} \n🌙 Iftar: {shom_iftor.time()} \n\n📅 Bugungi sanasi: {data['date']} \n\n {duo_text}",
            reply_markup=menuButtons)
        await state.clear()

    except KeyError:
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")


@dp.message(F.text == back, StateFilter(None))
async def back_handler(message: types.Message) -> None:
    await message.answer("🏘 Asosiy menyuga qaytib keldik.", reply_markup=menuButtons)


@dp.message(ChatTypeFilter("private"))
async def not_handler(message: types.Message) -> None:
    await message.answer("🤷‍♂️ Nimadir noto‘g‘ri keti.")


async def main() -> None:
    db.connect()
    db.create_tables([User, Taqvim])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
