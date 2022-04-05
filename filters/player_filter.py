from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    key = 'is_private'

    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsAdmin(BoundFilter):
    key = 'is_admin'

    async def check(self, message: types.Message):
        admins = [746461090, 5131674802]
        return message.from_user.id in admins
