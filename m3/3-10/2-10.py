""" Задача - Асинхронный HTTP-запрос """

import asyncio, aiohttp
import json
import time

from aiohttp import ClientError, ClientSession


class Requests:
    def __init__(self, urls: list[str], file_path: str = None, limit: int = 100):
        self._urls = urls * 200
        self._file_path = file_path
        self._sema = asyncio.Semaphore(limit)

        self._responses = {}


    async def _fetch(self, url: str, session: ClientSession) -> dict:
        try:
            async with session.get(url) as response:
                status = response.status

        except (ClientError, asyncio.TimeoutError):
            status = 0

        finally:
            return {url: status}


    async def _sema_fetch(self, url: str, session: ClientSession) -> dict:
        async with self._sema:
            return await self._fetch(url, session)


    def _responses_to_file(self):
        with open(self._file_path, 'w') as file:
            json.dump(self._responses, file)
            print(self._responses)


    async def fetch_urls(self):
        tasks = []

        async with aiohttp.ClientSession() as session:
            for url in self._urls:
                tasks.append(asyncio.create_task(self._sema_fetch(url, session)))

            for task in asyncio.as_completed(tasks):
                result = await task
                self._responses.update(result)

        self._responses_to_file()


urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://nonexistent.url"
]


if __name__ == '__main__':
    client = Requests(urls, 'results.json')
    t = time.time()
    asyncio.run(client.fetch_urls())
    print(time.time() - t)



