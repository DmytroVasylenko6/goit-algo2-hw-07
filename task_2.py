import timeit
from functools import lru_cache

import matplotlib.pyplot as plt
from colorama import Fore, Style


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def splay(self, node, key):
        if not node:
            return node

        if key == node.key:
            return node

        if key < node.key:
            if not node.left:
                return node
            if key < node.left.key:
                node.left.left = self.splay(node.left.left, key)
                node = self.rotate_right(node)
            elif key > node.left.key:
                node.left.right = self.splay(node.left.right, key)
                if node.left.right:
                    node.left = self.rotate_left(node.left)
            return node if not node.left else self.rotate_right(node)
        else:
            if not node.right:
                return node
            if key < node.right.key:
                node.right.left = self.splay(node.right.left, key)
                if node.right.left:
                    node.right = self.rotate_right(node.right)
            return node if not node.right else self.rotate_left(node)

    def rotate_left(self, node):
        if not node or not node.right:
            return node
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def rotate_right(self, node):
        if not node or not node.left:
            return node
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if not node:
            return SplayTreeNode(key, value)
        node = self.splay(node, key)
        if key == node.key:
            node.value = value
        elif key < node.key:
            new_node = SplayTreeNode(key, value)
            new_node.left = node.left
            node.left = None
            node = self.rotate_right(node)
            new_node.right = node
            return new_node
        else:
            new_node = SplayTreeNode(key, value)
            new_node.right = node.right
            node.right = None
            node = self.rotate_left(node)
            new_node.left = node
            return new_node

    def find(self, key):
        self.root = self.splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None


def fibonacci_splay(n, tree):
    value = tree.find(n)
    if value is not None:
        return value
    if n <= 1:
        return n
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


def measure_time():
    ns = list(range(0, 1000, 50))
    lru_times = []
    splay_times = []

    tree = SplayTree()

    for n in ns:
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
        lru_times.append(lru_time)

        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
        splay_times.append(splay_time)

    return ns, lru_times, splay_times


def plot_results():
    ns, lru_times, splay_times = measure_time()

    print(
        f"{Fore.RED}{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)'}{Style.RESET_ALL}"
    )
    print(Fore.RED + "-" * 50 + Style.RESET_ALL)
    for n, lru_time, splay_time in zip(ns, lru_times, splay_times):
        print(f"{n:<10}{lru_time:<25}{splay_time}{Style.RESET_ALL}")

    plt.figure(figsize=(10, 6))
    plt.plot(ns, lru_times, label="LRU Cache")
    plt.plot(ns, splay_times, label="Splay Tree")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_results()
