from functools import wraps

import redis

redis_client = redis.StrictRedis(host='localhost', port=6379)


def single(max_processing_time=120):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = 'func_lock:' + func.__name__
            locked = redis_client.set(key, 1, nx=True, ex=max_processing_time)

            try:
                if locked:
                    return func(*args, **kwargs)
            finally:
                redis_client.delete(key)

        return wrapper
    return decorator



