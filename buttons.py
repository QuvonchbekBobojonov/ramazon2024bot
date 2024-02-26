from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from context import regions

btn1 = '🎁 Tabrik noma tayyorlash'
btn2 = '⏳ Taqvim ko‘rish'
back = '⬅️ Orqaga'

taqvimButtonToday_text = '📅 Bugungi taqvim'
taqvimButtonTomorrow_text = '📅 Ertangi taqvim'

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

taqvimButtons = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Taqvimni tanlang",
    keyboard=[
        [
            KeyboardButton(text=taqvimButtonToday_text),
            KeyboardButton(text=taqvimButtonTomorrow_text)
        ],
        [
            KeyboardButton(text=back)
        ]
    ]
)

designButtons = InlineKeyboardMarkup(
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



def regionsButtons():
    builder = InlineKeyboardBuilder()
    for key, value in regions:
        builder.button(text=value, callback_data=f"region_{key}")
    builder.adjust(2)
    return builder.as_markup()
