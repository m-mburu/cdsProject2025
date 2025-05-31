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
    """Return one random lowercase word of the given length."""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def _tst_worst_chain(n: int) -> List[str]:
    """
    Worst-case for a TST: each word is the previous word plus one 'a'.
      n=5  ->  ['a', 'aa', 'aaa', 'aaaa', 'aaaaa']
    The tree becomes a single '=' chain of depth ≈ n.
    """
    return ["a" * i for i in range(1, n + 1)]
print("Worst-case TST chain generated:", _tst_worst_chain(5))

def _tst_best_common_prefix(n: int,
                            prefix: str = "app",
                            suffix_len: int = 4) -> List[str]:
    """
    Best-case for a TST: many strings share a *long common prefix*.
    Every word is  <prefix> + random suffix.
    Example (prefix='app', n=4) ->  ['appxq', 'appdo', 'appgh', 'appjb']
    The TST follows '=' links for the shared prefix, then branches.
    """
    seen = set()
    while len(seen) < n:
        suffix = _random_word(suffix_len)
        seen.add(prefix + suffix)
    return list(seen)


def _median_order(seq: List[str]) -> List[str]:
    """Return the list reordered in median-first order (keeps BST/TST balanced)."""
    if not seq:
        return []
    mid = len(seq) // 2
    return [seq[mid]] + _median_order(seq[:mid]) + _median_order(seq[mid + 1:])


def generate_words(n: int,
                   *,
                   k: int | None = None,
                   case: Case = "average",
                   seed: int | None = None) -> List[str]:
    """
    Produce a list of *unique* words tailored to the chosen case.

    - average : fully random words of length k (or 2–20 if k is None), shuffled.
    - best    : words that all share a long common prefix (good for TST).
    - worst   : 'a', 'aa', 'aaa', … — forces a degenerate '=' chain.
    """
    if seed is not None:
        random.seed(seed)

    if case == "worst":
        return _tst_worst_chain(n)

    if case == "best":
        
        words = _tst_best_common_prefix(n, prefix="app", suffix_len=4)
        return _median_order(sorted(words))

    # 
    word_len = k if k is not None else random.randint(2, 20)
    pool = set()
    while len(pool) < n:
        pool.add(_random_word(word_len))
    words = list(pool)
    random.shuffle(words)
    return words


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
