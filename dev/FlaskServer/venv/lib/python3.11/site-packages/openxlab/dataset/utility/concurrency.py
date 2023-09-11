from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from typing import Callable
from typing import Iterable


def concurrent_submit(func: Callable, workers: int, *args):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        pool = [executor.submit(func, *args) for i in range(workers)]
        results = [f.result() for f in pool]
        return results


def concurrent_map(func: Callable, workers: int, iters: Iterable):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(func, iters)
        return results


if __name__ == "__main__":
    print("+++++++++++++++ test ++++++++++++++++++")
    t_list = [1, 2, 3, 4, 5]
    concurrent_map(lambda x: print(x + 1), 5, t_list)
    print(t_list)
