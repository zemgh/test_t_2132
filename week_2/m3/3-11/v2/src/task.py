from typing import Callable


class Task:
    def __init__(self, message: dict, done_func: Callable):
        self._message = message
        self._done_func = done_func

    @property
    def message(self):
        return self._message

    async def done(self):
        await self._done_func(self._message)