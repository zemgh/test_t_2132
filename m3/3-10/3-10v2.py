""" Задача - Асинхронный HTTP-запрос """

import asyncio, aiohttp
import json
import time

from aiohttp import ClientError


class Requests:
    def __init__(self, urls: list[str], file_path: str, limit: int = 1000):
        self._urls = iter(urls * 10000)
        self._file_path = file_path
        self._limit = limit

        self._responses = []

    async def _fetch(self, url: str, session: aiohttp.ClientSession) -> dict:
        try:
            async with session.get(url) as response:
                status = response.status

        except (ClientError, asyncio.TimeoutError):
            status = 0

        finally:
            return {url: status}

    async def _test_task(self, *args):
        await asyncio.sleep(0.1)
        return {'task': 'test'}


    def _get_url(self):
        try:
            return next(self._urls)
        except StopIteration:
            return None

    async def _worker(self, func, session: aiohttp.ClientSession):
        while True:

            url = self._get_url()
            if not url:
                break

            response = await func(url, session)
            self._responses.append(response)


    def _responses_to_file(self):
        with open(self._file_path, 'w') as file:
            json.dump(self._responses, file)


    async def fetch_urls(self):
        async with aiohttp.ClientSession() as session:
            task = self._test_task

            workers = [
                asyncio.create_task(
                    self._worker(task, session)
                )
                for _ in range(self._limit)
            ]

            await asyncio.gather(*workers)

        self._responses_to_file()


urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]


if __name__ == '__main__':
    client = Requests(urls, 'results.json')
    t = time.time()
    asyncio.run(client.fetch_urls())
    print(time.time() - t)