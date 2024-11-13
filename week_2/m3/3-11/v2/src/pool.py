import asyncio
from typing import Optional, List

from src.worker import BrokenBaseWorker
from src.list_queue import RedisListQueue
from src.monitor import RedisListQueueMonitor


class WorkersPool:
    def __init__(self,
                 worker: BrokenBaseWorker,
                 max_workers: int,
                 queue: RedisListQueue,
                 queue_monitor: Optional[RedisListQueueMonitor] = None,
                 ):

        self._worker_cls = worker
        self._max_workers = max_workers
        self._workers: List[BrokenBaseWorker] = []
        self._workers_tasks: List[asyncio.Task] = []

        self._queue = queue
        self._queue_monitor = queue_monitor
        self._monitor_task: Optional[asyncio.Task] = None

        self._running: bool = False

    async def start(self):
        self._running = True

        for i in range(self._max_workers):
            worker = self._worker_cls(i, self._queue)
            self._workers.append(worker)
            self._workers_tasks.append(asyncio.create_task(worker.run()))

        if self._queue_monitor:
            self._monitor_task = asyncio.create_task(self._queue_monitor.run())


    async def stop(self):
        self._running = False

        for task in self._workers_tasks:
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

        if self._monitor_task:
            self._monitor_task.cancel()

            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

    async def run_forever(self):
        await self.start()

        try:
            while self._running:
                await asyncio.sleep(1)
        finally:
            await self.stop()