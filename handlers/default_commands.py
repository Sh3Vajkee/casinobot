from textwrap import dedent
from aiogram import types, Dispatcher

from db.models import PlayerBalance
from keyboars import get_spin_keyboard
from filters.player_filter import IsPrivate

flags = {"throttling_key": "default"}


async def cmd_start(message: types.Message):
    db_session = message.bot.get('db')

    async with db_session() as session:
        player: PlayerBalance = await session.get(PlayerBalance, message.from_user.id)

    if player:

        start_text = f"Привет, {player.user_name}!\nТвой баланс - <b>{player.balance}pts</b>"
        await message.answer(dedent(start_text).format(points=player.balance), reply_markup=get_spin_keyboard())

    else:
        try:
            user_name = f'@{message.from_user.username}'
        except:
            user_name = f'User_{message.from_user.id}'

        async with db_session() as session:
            new_player: PlayerBalance = await session.merge(
                PlayerBalance(
                    user_id=message.from_user.id,
                    user_name=user_name,
                    balance=50
                )
            )
            await session.commit()
        start_text = """\
        <b>Добро пожаловать в наше виртуальное казино!</b>
        У вас {points} очков. Каждая попытка стоит 1 очко, а за выигрышные комбинации вы получите:

        3 одинаковых символа (кроме семёрки) — 7 очков
        7️⃣7️⃣▫️ — 5 очков (квадрат = что угодно)
        7️⃣7️⃣7️⃣ — 10 очков

        <b>Внимание</b>: бот предназначен исключительно для демонстрации, и ваши данные могут быть сброшены в любой момент!
        Помните: лудомания — это болезнь, и никаких платных опций в боте нет.

        Убрать клавиатуру — /stop
        Показать клавиатуру, если пропала — /spin
        """
        await message.answer(dedent(start_text).format(points=new_player.balance), reply_markup=get_spin_keyboard())


async def cmd_stop(message: types.Message):
    await message.answer("Клавиатура удалена. Вернуть клавиатуру и продолжить: /spin", reply_markup=types.ReplyKeyboardRemove())


async def cmd_help(message: types.Message):
    help_text = \
        "В казино доступно 4 элемента: BAR, виноград, лимон и цифра семь. Комбинаций, соответственно, 64. " \
        # "Для распознавания комбинации используется четверичная система, а пример кода " \
    # "для получения комбинации по значению от Bot API можно увидеть " \
    # "<a href='https://gist.github.com/MasterGroosha/963c0a82df348419788065ab229094ac'>здесь</a>.\n\n"
    await message.answer(help_text, disable_web_page_preview=True)


def default_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, IsPrivate(), commands='start')
    dp.register_message_handler(cmd_stop, IsPrivate(), commands='stop')
    dp.register_message_handler(cmd_help, IsPrivate(), commands='help')
