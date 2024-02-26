from aiogram.fsm.state import StatesGroup, State


class GiftState(StatesGroup):
    design = State()
    name = State()
    author = State()

