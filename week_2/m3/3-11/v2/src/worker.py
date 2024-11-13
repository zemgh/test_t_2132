import random

from src.list_queue import RedisListQueue
from src.task import Task


class BrokenBaseWorker:
    def __init__(self, worker_id: int, queue: RedisListQueue):
        self._worker_id = worker_id
        self._queue = queue

    @property
    def worker_id(self) -> int:
        return self._worker_id

    async def run(self):
        while True:
            task: Task = await self._queue.consume()

            # The worker is trying very hard to do his job, but something can go wrong
            broken = True if random.randint(0, 3) == 0 else False
            if not broken:
                await self._execute(task)
                await task.done()

    async def _execute(self, task: Task):
        raise NotImplementedError


class PrintWorker(BrokenBaseWorker):
    async def _execute(self, task: Task):
        print(task.message)
