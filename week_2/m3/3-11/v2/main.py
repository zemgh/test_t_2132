import asyncio
import random

from redis.asyncio import Redis

from src.list_queue import RedisListQueue
from src.monitor import RedisListQueueMonitor
from src.pool import WorkersPool
from src.worker import PrintWorker


async def add_tasks(queue: RedisListQueue):
    async def add():
        for _ in range(3):
            await queue.publish(
                {str(random.randint(0, 10000)): random.randint(0, 10000)}
            )

    while True:
        await add()
        await asyncio.sleep(5)


async def main():
    queue_name = 'test_list_queue'
    redis_cli = Redis()
    queue = RedisListQueue(redis_cli, queue_name)
    monitor = RedisListQueueMonitor(redis_cli, queue_name)
    pool = WorkersPool(PrintWorker, max_workers=1, queue=queue, queue_monitor=monitor)

    await asyncio.gather(
        asyncio.create_task(pool.run_forever()),
        asyncio.create_task(add_tasks(queue))
    )


if __name__ == '__main__':
    asyncio.run(main())


