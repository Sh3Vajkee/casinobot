from aiogram import types


def get_spin_keyboard():
    keyboard = [
        [types.KeyboardButton(text='🎰 Испытать удачу!')]
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
