from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

btn1 = '🎁 Tabrik noma tayyorlash'
btn2 = '⏳ Taqvim ko‘rish'

menuButtons = ReplyKeyboardMarkup(
    resize_keyboard=True,
    is_persistent=True,
    keyboard=[
        [
            KeyboardButton(text=btn2)
        ],
        [
            KeyboardButton(text=btn1)
        ]
    ],
)
