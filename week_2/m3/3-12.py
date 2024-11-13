import time
import uuid

import redis
import requests
from requests import Request


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, redis_cli: redis.Redis, delta: int = 3, limit: int = 5):
        self._redis_cli = redis_cli
        self._delta = delta
        self._limit = limit

    def test(self, host: str) -> bool:
        now = time.time()
        start_time = now - self._delta
        key = self._get_key(host)

        count = self._redis_cli.zcount(key, start_time, now)
        return count < self._limit

    def add_request(self, host: str):
        timestamp = time.time()
        request_id = str(uuid.uuid4())
        key = self._get_key(host)

        self._redis_cli.zadd(key, {request_id: timestamp})

    def _get_key(self, host: str) -> str:
        return f'rate_limit:{host}'


def make_api_request(host: str, url: str, rate_limiter: RateLimiter):
    if not rate_limiter.test(host):
        raise RateLimitExceed
    else:
        rate_limiter.add_request(host)
        response = requests.get(url)


if __name__ == '__main__':
    host = 'yandex.ru'
    url = 'http://yandex.ru'
    redis_cli = redis.Redis()
    rate_limiter = RateLimiter(redis_cli)

    for _ in range(50):
        time.sleep(0.2)

        try:
            make_api_request(host, url, rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")