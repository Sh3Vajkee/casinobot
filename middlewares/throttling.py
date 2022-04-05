from cachetools import TTLCache
import asyncio
from math import inf

from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


caches = {
    "default": TTLCache(maxsize=inf, ttl=1),
    "spin": TTLCache(maxsize=inf, ttl=2)
}


def rate_limit(key="spin"):

    def decorator(func):
        setattr(func, 'throttling_key', key)
        return func
    return decorator


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=2, key_prefix='antoflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):

        handler = current_handler.get()

        dispatcher = Dispatcher.get_current()

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key',
                          f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            raise CancelHandler()

    # async def message_throttled(self, message: types.Message, throttled: Throttled):

    #     handler = current_handler.get()
    #     dispatcher = Dispatcher.get_current()

    #     if handler:
    #         key = getattr(handler, 'throttling_key',
    #                       f"{self.prefix}_{handler.__name__}")
    #     else:
    #         key = f"{self.prefix}_message"

    #     delta = throttled.rate - throttled.delta

    #     await asyncio.sleep(delta)

        # if throttling_key and throttling_key in caches:
        #     if not caches[throttling_key].get(message.chat.id):
        #         caches[throttling_key][message.chat.id] = True
        #         return
        #     else:
        #         raise CancelHandler
