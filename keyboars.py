from aiogram import types


def get_spin_keyboard():
    keyboard = [
        [types.KeyboardButton(text='๐ฐ ะัะฟััะฐัั ัะดะฐัั!')]
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
