from asyncio import sleep
from textwrap import dedent

from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types

from keyboars import get_spin_keyboard
from handlers.dice_check import get_combo_data
from filters.player_filter import IsPrivate
from db.models import PlayerBalance


async def cmd_spin(message: types.Message):
    db_session = message.bot.get('db')

    async with db_session() as session:
        player: PlayerBalance = await session.get(PlayerBalance, message.from_user.id)

    balance = player.balance
    if balance == 0:
        await message.answer_sticker("CAACAgIAAxkBAAEFGxpfqmqG-MltYIj4zjmFl1eCBfvhZwACuwIAAuPwEwwS3zJY4LIw9B4E")
        await message.answer(
            "Ваш баланс равен нулю. Вы можете смириться с судьбой и продолжить жить своей жизнью, "

        )
        return

    answer_text_template = "Ваша комбинация:\n{combo_text} (№{dice_value}).\n{win_or_lose_text}\nВаш счёт: <b>{new_score}</b>."

    msg = await message.answer_dice(emoji="🎰", reply_markup=get_spin_keyboard())
    score_change, combo_text = get_combo_data(msg.dice.value)

    if score_change < 0:
        win_or_lose_text = "Вы проиграли"
    else:
        win_or_lose_text = f"Вы выиграли {score_change} очков"

    async with db_session() as session:
        player: PlayerBalance = await session.get(PlayerBalance, message.from_user.id)
        player.balance += score_change
        await session.commit()

    new_score = balance + score_change

    await sleep(2)
    await message.reply(
        dedent(answer_text_template).format(
            combo_text=combo_text,
            dice_value=msg.dice.value,
            win_or_lose_text=win_or_lose_text,
            new_score=new_score
        )
    )


def spin_hanlders(dp: Dispatcher):
    dp.register_message_handler(cmd_spin, IsPrivate(), commands='spin')
    dp.register_message_handler(
        cmd_spin, IsPrivate(), Text(equals='🎰 Испытать удачу!'))
