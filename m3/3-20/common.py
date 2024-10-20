import itertools
import multiprocessing
import random


def get_ranges(n: int, count: int) -> list:
    ranges = []
    chunk_size = n // count

    start = 1
    for i in range(1, count):
        end = start + chunk_size
        r = range(start, end)
        ranges.append(r)
        start = end

    ranges.append(range(start, n + 1))
    assert len(ranges) == count

    return ranges


def generate_random_numbers(r: range) -> list[int]:
    return [random.randint(1, 1000) for _ in r]


def calculate_factorial(r: range) -> int:
    result = 1
    for i in r:
        result *= i
    return result


def worker_factorials(r: range, queue: multiprocessing.Queue):
    result = calculate_factorial(r)
    queue.put(result)


def worker_random_numbers(r: range, queue: multiprocessing.Queue):
    result = generate_random_numbers(r)
    queue.put(result)


def unpack_lists(lists: list) -> list:
    return list(itertools.chain.from_iterable(lists))

