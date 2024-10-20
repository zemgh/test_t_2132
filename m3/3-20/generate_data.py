import concurrent.futures
import multiprocessing

from common import get_ranges, generate_random_numbers, worker_random_numbers, unpack_lists


def generate_data_mp_pool(count: int, cpu_count: int) -> list[int]:
    ranges = get_ranges(count, cpu_count)

    with multiprocessing.Pool(processes=cpu_count) as pool:
        results = pool.map(generate_random_numbers, ranges)
        return unpack_lists(results)


def generate_data_mp_queue(count: int, cpu_count: int) -> list[int]:
    results = []
    processes = []
    ranges = get_ranges(count, cpu_count)
    queue = multiprocessing.Queue()

    try:
        for r in ranges:
            p = multiprocessing.Process(target=worker_random_numbers, args=(r, queue))
            processes.append(p)
            p.start()

        for _ in ranges:
            results.append(queue.get())

        for p in processes:
            p.join()

        return unpack_lists(results)

    except Exception as e:
        print(e)


def generate_data_thread_executor(count: int, threads_count: int) -> list[int]:
    ranges = get_ranges(count, threads_count)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_count) as executor:
        results = executor.map(generate_random_numbers, ranges)
        return unpack_lists(results)


def generate_data_base(count: int, cpu_count=None) -> list[int]:
    return generate_random_numbers(range(1, count+1))
