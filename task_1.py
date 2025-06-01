import random
import time
from collections import OrderedDict


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


def range_sum_no_cache(array, left, right):
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    array[index] = value


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, index):
        keys_to_delete = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_delete:
            del self.cache[key]


cache = LRUCache(1000)


def range_sum_with_cache(array, left, right):
    key = (left, right)
    cached = cache.get(key)
    if cached != -1:
        return cached
    result = sum(array[left : right + 1])
    cache.put(key, result)
    return result


def update_with_cache(array, index, value):
    array[index] = value
    cache.invalidate(index)


def main():
    N = 100_000
    Q = 50_000
    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array, query[1], query[2])
        else:
            update_no_cache(array, query[1], query[2])
    time_no_cache = time.time() - start

    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array, query[1], query[2])
        else:
            update_with_cache(array, query[1], query[2])
    time_with_cache = time.time() - start

    print(f"Без кешу :  {time_no_cache:.2f} c")
    print(f"LRU-кеш  :  {time_with_cache:.2f} c", end="")
    if time_with_cache < time_no_cache:
        speedup = time_no_cache / time_with_cache
        print(f"  (прискорення ×{speedup:.1f})")
    else:
        print("  (кеш не дав приросту продуктивності)")


if __name__ == "__main__":
    main()
