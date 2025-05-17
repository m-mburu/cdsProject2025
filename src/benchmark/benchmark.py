# Benchmarking script for HPC performance tests
import psutil
import os
import random
import string
import time
import pandas as pd
from collections import defaultdict
from typing import List, Literal

Case = Literal["average", "best", "worst"]


def _random_word(length: int) -> str:
    """Generate a random word of given length.
    :param length: Length of the word
    :return: Random word
    """
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def _median_order(seq: List[str]) -> List[str]:
    """
    Generate a median order of the sequence for balanced insertion.
    :param seq: List of strings
    :return: Median ordered list
    """

    if not seq:
        return []
    mid = len(seq) // 2
    return [seq[mid]] + _median_order(seq[:mid]) + _median_order(seq[mid+1:])


def generate_words(n: int,
                   k: int | None = None,
                   case: Case = "average",
                   seed: int | None = None) -> List[str]:
    """
    Generate a list of random words for benchmarking.
    :param n: Number of words to generate
    :param k: Length of each word (if None, random length between 2 and 20)
    :param case: Type of order for the words
    :param seed: Random seed for reproducibility
    :return: List of generated words
    """
    if seed is not None:
        random.seed(seed)

    #  generate unique words
    word_len = k if k is not None else None
    pool = set()
    while len(pool) < n:
        pool.add(_random_word(word_len or random.randint(2, 20)))
    words = sorted(pool)                    

    # requested cases
    # average cases
    if case == "average":
        random.shuffle(words)               
        return words

    if case == "worst":
        return words                     
    # best case; median ordered ordered
    if case == "best":
        return _median_order(words)        

    raise ValueError(f"Unknown case: {case!r}")


def get_ram_usage_mb():
    """
    Get the current RAM usage of the process in MB.
    :return: RAM usage in MB
    """
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1e6  # MB
    return mem


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


def run_comparison(
        sizes: list[int],
        tree_specs: list[tuple[str, type]],
        repeat: int = 3,
        case: str = "average",
        *,
        verbose: bool = True
) -> pd.DataFrame:
    """
    Benchmark multiple tree classes on the same word lists.

    Parameters
    ----------
    sizes      : list of word-set sizes to test
    tree_specs : list of (label, TreeClass) tuples, e.g.
                 [("tst", TSTree), ("bst", Btree)]
    repeat     : repetitions passed straight to `benchmark_tree`
    case       : "average" | "best" | "worst"
    verbose    : print progress if True

    Returns
    -------
    pd.DataFrame in wide format — one row per `size`,
    columns "<label>_<metric>" for metric in {insert, search, ram}.
    """
    # build an empty dict-of-lists with dynamic keys ---------------
    results = defaultdict(list)
    results["size"] = []           # always present

    for label, _ in tree_specs:
        for metric in ("insert", "search", "ram"):
            results[f"{label}_{metric}"] = []

    # --------------------------------------------------------------
    for size in sizes:
        words = generate_words(size, case=case)

        if verbose:
            print(f"\nBenchmarking {size} words ({case} case)…")

        row_metrics = {}           # temporary store for pretty printing

        for label, TreeClass in tree_specs:
            ins, srch, ram = benchmark_tree(TreeClass, words, repeat)
            results[f"{label}_insert"].append(ins)
            results[f"{label}_search"].append(srch)
            results[f"{label}_ram"].append(ram)

            row_metrics[label] = (ins, srch, ram)

        results["size"].append(size)

        if verbose:
            for label, (ins, srch, ram) in row_metrics.items():
                print(f"{label:<8}| ins {ins:.4f}s | srch {srch:.4f}s | ram {ram:.2f} MB")

    return pd.DataFrame(results)
