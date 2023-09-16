from aiogram.dispatcher.filters.state import StatesGroup, State


class quiz(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()

class answering(StatesGroup):
	ans = State()

    