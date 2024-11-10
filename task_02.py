import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

def factorize_sync(*numbers):
    results = []
    for number in numbers:
        factors = [i for i in range(1, number + 1) if number % i == 0]
        results.append(factors)
    return results


def factorize_parallel(*numbers):
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        results = list(executor.map(find_factors, numbers))
    return results

def find_factors(number):
    return [i for i in range(1, number + 1) if number % i == 0]


if __name__ == "__main__":
    numbers_to_factorize = [128, 255, 99999, 10651060]

    start_time = time.time()
    sync_result = factorize_sync(*numbers_to_factorize)
    sync_duration = time.time() - start_time
    print(f"Synchronous execution time: {sync_duration:.4f} seconds")

    start_time = time.time()
    parallel_result = factorize_parallel(*numbers_to_factorize)
    parallel_duration = time.time() - start_time
    print(f"Parallel execution time: {parallel_duration:.4f} seconds")

    expected_results = [
        [1, 2, 4, 8, 16, 32, 64, 128],
        [1, 3, 5, 15, 17, 51, 85, 255],
        [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999],
        [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 
         380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    ]

    assert sync_result == expected_results, "Synchronous result is incorrect"
    assert parallel_result == expected_results, "Parallel result is incorrect"

    print("Both synchronous and parallel implementations are correct.")