import json
import time

from typing import Optional
from redis.asyncio import Redis

from src.task import Task


class RedisListQueue:
    def __init__(self, redis_cli: Redis, queue_name: str, timeout: int = 15):
        self._redis_cli = redis_cli
        self._queue_name = queue_name
        self._processing_queue = f'{self._queue_name}:processing'
        self._processing_times = f'{self._queue_name}:times'
        self._timeout = timeout

    async def publish(self, msg: dict):
        await self._redis_cli.lpush(self._queue_name, json.dumps(msg))

    async def consume(self) -> Optional[Task]:
        data = await self._redis_cli.brpoplpush(self._queue_name, self._processing_queue, timeout=self._timeout)
        if data:
            await self._redis_cli.hset(self._processing_times, data, time.time())
            task = Task(json.loads(data), self._ack)
            return task

    async def _ack(self, msg: dict):
        msg = json.dumps(msg)
        await self._redis_cli.lrem(self._queue_name, 1, msg)
        await self._redis_cli.hdel(self._processing_times, msg)
        # log