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

designButtons = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 - dizayn", callback_data="design_1"),
            InlineKeyboardButton(text="2 - dizayn", callback_data="design_2"),
            InlineKeyboardButton(text="3 - dizayn", callback_data="design_3")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="design_back")
        ]
    ]
)
