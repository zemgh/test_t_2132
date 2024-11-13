import json
from typing import Optional

from redis import Redis


class RedisListQueue:
    def __init__(self, redis_cli: Redis, queue_name: str, timeout: int = 0):
        self.redis_cli = redis_cli
        self.queue_name = queue_name
        self.timeout = timeout

    def publish(self, msg: dict):
        self.redis_cli.lpush(self.queue_name, json.dumps(msg))

    def consume(self) -> Optional[dict]:
        data = self.redis_cli.brpop(self.queue_name, timeout=self.timeout)
        if data:
            queue, msg = data
            return json.loads(msg)


if __name__ == '__main__':
    redis_cli = Redis()
    q = RedisListQueue(redis_cli, 'test_list_queue', timeout=3)

    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
