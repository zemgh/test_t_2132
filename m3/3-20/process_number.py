import concurrent.futures
import multiprocessing
import math

from common import get_ranges, calculate_factorial, worker_factorials


def process_number_mp_pool(n: int, cpu_count: int) -> int:
    ranges = get_ranges(n, cpu_count)

    with multiprocessing.Pool(processes=cpu_count) as pool:
        results = pool.map(calculate_factorial, ranges)
        return math.prod(results)


def process_number_mp_queue(n: int, cpu_count: int) -> int:
    results = []
    processes = []
    ranges = get_ranges(n, cpu_count)
    queue = multiprocessing.Queue()

    try:
        for r in ranges:
            p = multiprocessing.Process(target=worker_factorials, args=(r, queue))
            processes.append(p)
            p.start()

        for _ in ranges:
            results.append(queue.get())

        for p in processes:
            p.join()

        return math.prod(results)

    except Exception as e:
        print(e)


def process_number_thread_executor(n: int, threads_count: int) -> int:
    ranges = get_ranges(n, threads_count)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_count) as executor:
        results = executor.map(calculate_factorial, ranges)
        return math.prod(results)


def process_number_base(n: int, cpu_count=None) -> int:
    r = range(1, n)
    return calculate_factorial(r)
