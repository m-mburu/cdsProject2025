# Benchmarking script for HPC performance tests
import psutil
import os
import random
import string
import time

def generate_words(n, k= None):
    """
    Generate a list of n random words.
    Each word is a random string of lowercase letters with a length between 2 and 20.
    :param n: Number of words to generate
    :return: List of random words
    """
    # Generate n random words
    if k is None:
        k = random.randint(2, 20)
    return [''.join(random.choices(string.ascii_lowercase, k= k)) for _ in range(n)]


def get_ram_usage_mb():
    """
    Get the current RAM usage of the process in MB.
    :return: RAM usage in MB
    """
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1e6  # MB
    return  mem

def benchmark_tree(TreeClass, words, repeat=50):
    """
    Benchmark the insert and search operations of a tree data structure.
    :param TreeClass: The tree class to be benchmarked
    :param words: List of words to insert and search
    :param repeat: Number of times to repeat the benchmark
    :return: Average insert time, average search time, and average memory usage
    """

    insert_times = []
    search_times = []
    memory_usages = []

    for _ in range(repeat):
        # Measure memory before building tree
        mem_before = get_ram_usage_mb()

        tree = TreeClass()

        # Insert benchmark
        start = time.perf_counter()
        for word in words:
            tree.insert(word)
        insert_duration = time.perf_counter() - start

        # Measure memory after building tree
        mem_after = get_ram_usage_mb()
        memory_usages.append(max(0, mem_after - mem_before))

        # Search benchmark
        start = time.perf_counter()
        for word in words:
            tree.search(word)
        search_duration = time.perf_counter() - start

        insert_times.append(insert_duration)
        search_times.append(search_duration)

    avg_insert = sum(insert_times) / repeat
    avg_search = sum(search_times) / repeat
    avg_memory = sum(memory_usages) / repeat
    return avg_insert, avg_search, avg_memory