""" Задача - Параллельная обработка числовых данных """

import json

from tests import test_process_number, test_generate_data


if __name__ == "__main__":
    results = {
        'process_number': {'n': None, 'results': None},
        'generate_data': {'n': None, 'results': None}
    }

    n = 300000
    results['process_number']['n'] = n
    results['process_number']['results'] = test_process_number(n)

    n = 10000000
    results['generate_data']['n'] = n
    results['generate_data']['results'] = test_generate_data(n)

    with open('results.json', 'w') as file:
        json.dump(results, file)
