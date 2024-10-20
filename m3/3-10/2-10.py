""" Задача - Асинхронный HTTP-запрос """

import asyncio, aiohttp
import json
import typing

from aiohttp import ClientConnectorError


class Requests:
    def __init__(self, urls: list[str], file_path: str = None, limit: int = 5):
        self._urls = urls
        self._file_path = file_path
        self._sema = asyncio.Semaphore(limit)

        self._responses = {}


    async def _fetch(self, url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    status = response.status

            except ClientConnectorError:
                status = 0

            finally:
                self._responses[url] = status


    async def _sema_fetch(self, url: str):
        async with self._sema:
            return await self._fetch(url)


    def _responses_to_file(self):
        with open(self._file_path, 'w') as file:
            json.dump(self._responses, file)


    async def fetch_urls(self):
        tasks = []
        for url in self._urls:
            tasks.append(asyncio.create_task(self._sema_fetch(url)))

        await asyncio.gather(*tasks)

        self._responses_to_file()



urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


if __name__ == '__main__':
    client = Requests(urls, 'results.json')
    result = asyncio.run(client.fetch_urls())



