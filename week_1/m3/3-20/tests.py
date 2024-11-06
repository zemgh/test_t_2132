import time

import process_number as process
import generate_data as gen


def test_func(func, n: int) -> dict:
    processes_workers_count = 8

    t1 = time.time()
    func(n, processes_workers_count)
    t2 = time.time()
    t = round(t2 - t1, 4)

    return {
        func.__name__: t
    }


def get_test_results(functions: list, n: int) -> dict:
    DELAY = 0.2
    results = []

    for f in functions:
        time.sleep(DELAY)
        r = test_func(f, n)
        results.append(r)
        time.sleep(DELAY)

    return results


def test_process_number(n: int) -> dict:
    functions = [
        process.process_number_mp_pool,
        process.process_number_mp_queue,
        process.process_number_thread_executor,
        process.process_number_base]

    return get_test_results(functions, n)


def test_generate_data(n: int) -> dict:
    functions = [
        gen.generate_data_mp_pool,
        gen.generate_data_mp_queue,
        gen.generate_data_thread_executor,
        gen.generate_data_base
    ]

    return get_test_results(functions, n)