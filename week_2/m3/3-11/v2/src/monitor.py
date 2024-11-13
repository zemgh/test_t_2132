import asyncio
import time
from typing import Union

from redis.asyncio import Redis


class RedisListQueueMonitor:
    def __init__(self, redis_cli: Redis, queue_name: str, retry_timeout: Union[int, float] = 5, delay: int = 3):
        self._redis_cli = redis_cli
        self._queue_name = queue_name
        self._processing_queue = f'{self._queue_name}:processing'
        self._processing_times = f'{self._queue_name}:times'
        self._retry_timeout = float(retry_timeout) if type(retry_timeout) is int else retry_timeout
        self._delay = delay

    async def run(self):
        while True:
            await asyncio.sleep(self._delay)
            await self._check_stuck_tasks()

    async def _check_stuck_tasks(self):
        current_time = time.time()
        stuck_tasks = []
        tasks = await self._redis_cli.hgetall(self._processing_times)

        for task, add_time in tasks.items():

            decoded_add_time = float(add_time.decode('utf-8'))
            if current_time - decoded_add_time > self._retry_timeout:
                decoded_task = task.decode('utf-8')
                stuck_tasks.append(decoded_task)

        print('stuck_tasks', stuck_tasks)

        for task in stuck_tasks:
            await self._redis_cli.lrem(self._processing_queue, 1, task)
            await self._redis_cli.hdel(self._processing_times, task)
            await self._redis_cli.rpush(self._queue_name, task)