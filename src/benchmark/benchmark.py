# Benchmarking script for HPC performance tests
import psutil
import os
import random
import string
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def generate_words(n: int, k: int = None) -> list[str]:
    """
    Generate a list of n random words consisting of lowercase letters.

    Parameters:
        n (int): Number of words to generate.
        k (int, optional): If specified, all words will be of fixed length k.
                           If None, each word will have a random length between 2 and 20.

    Returns:
        list[str]: A list of randomly generated words.
    """
    words = []

    for _ in range(n):
        word_length = k if k is not None else random.randint(2, 20)
        word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        words.append(word)

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


def run_comparison(sizes, repeat=3):
    results = {
        "size": [],
        "tst_insert": [],
        "tst_search": [],
        "tst_ram": [],
        "bst_insert": [],
        "bst_search": [],
        "bst_ram": []
    }

    for size in sizes:
        words = generate_words(size)
        print(f"\nBenchmarking {size} words...")

        t_ins, t_srch, t_ram = benchmark_tree(TSTree, words, repeat)
        b_ins, b_srch, b_ram = benchmark_tree(Btree, words, repeat)

        results["size"].append(size)
        results["tst_insert"].append(t_ins)
        results["tst_search"].append(t_srch)
        results["tst_ram"].append(t_ram)
        results["bst_insert"].append(b_ins)
        results["bst_search"].append(b_srch)
        results["bst_ram"].append(b_ram)

        print(f"TSTree  | Insert: {t_ins:.4f}s | Search: {t_srch:.4f}s | RAM: {t_ram:.2f} MB")
        print(f"Btree   | Insert: {b_ins:.4f}s | Search: {b_srch:.4f}s | RAM: {b_ram:.2f} MB")

    return results


def plot_facet_metrics(df):

    # Melt the DataFrame
    df_melted = df.melt(
        id_vars="size",
        value_vars=["tst_insert", "tst_search", "tst_ram", "bst_insert", "bst_search", "bst_ram"],
        var_name="metric", value_name="value"
    )

    # Extract 'tree' and 'test_type', then drop 'metric'
    df_melted[["tree", "test_type"]] = df_melted["metric"].str.extract(r'^(tst|bst)_(.*)$')
    df_melted = df_melted.drop(columns=["metric"])

    # Plot using Seaborn FacetGrid (relplot)
    g = sns.relplot(
        data=df_melted,
        x="size", y="value",
        col="test_type", hue="tree", kind="line",
        facet_kws={'sharey': False, 'sharex': True},
        height=4, aspect=1.2
    )
    g.set_titles("{col_name}")
    g.set_axis_labels("Number of Words", "Value")
    g.fig.suptitle("TSTree vs Btree: Performance Metrics", y=1.05)
    plt.show()
