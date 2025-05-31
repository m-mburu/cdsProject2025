import random
import os
import pandas as pd
import sys

from src.tstree.tstree import TSTree
from src.btree.btree import Btree
from src.benchmark.benchmark import run_comparison
from typing import List

sys.setrecursionlimit(100_000)  
def run_cron_comparison(person_name: str | None, sizes: List[int], repeat: int):
    """
    Runs the comparison and saves the results to a CSV file.
    This function performs a series of comparisons using the TSTree and Btree
    data structures, generating datasets of specified sizes and repeating the

    :param:`repeat` number of times for each size.
    :param person_name: Optional name to include in the filename.
    :param sizes: List of dataset sizes to benchmark.
    :param repeat: Number of times to repeat each benchmark for averaging.
    :return: None
    """
    random.seed(100)
    
    df_best = run_comparison(sizes, tree_specs=[("tst", TSTree), ("bst", Btree)], repeat=repeat, case="best")
    df_worst = run_comparison(sizes, tree_specs=[("tst", TSTree), ("bst", Btree)], repeat=repeat, case="worst")
    df_average = run_comparison(sizes, tree_specs=[("tst", TSTree), ("bst", Btree)], repeat=repeat, case="average")
    
    # Combine results
    df = pd.concat([df_best, df_worst, df_average], keys=["best", "worst", "average"], names=["case"])

    # check if data/ directory exists
    os.makedirs("data", exist_ok=True)
    
    # Build filename
    if person_name:
        filename = f"data/df_{person_name.lower()}.csv"
    else:
        filename = "data/df.csv"
    
    df.to_csv(filename, index=True)
    print(f"Saved results to {filename}")
    print(df)


def generate_sizes(hpc: bool = False,
                   max_n: int | None = None) -> List[int]:
    """
    Return a list of dataset sizes for benchmarking.

    :param hpc : bool, default False
         False   sizes span 1e4 … 5e5  (quick local runs)  
         True   sizes start at 1e6 and grow up to `max_n`
    :param  max_n : int, optional
        Only used when `hpc=True`.  Hard upper bound for the sequence.
        Defaults to 5_000_000 (5 M).
    """
    if not hpc:
        return [5_000, 10_000, 15_000]
    if max_n is None:
        max_n = 5_000_000

    sizes, n, factor = [], 1_000_000, 2.0
    while n <= max_n:
        sizes.append(n)
        factor = 2.5 if factor == 2.0 else 2.0
        n = int(n * factor)

    return sizes


if __name__ == "__main__":

    # Read command-line arguments: sys.argv[1], sys.argv[2] (optional), and sys.argv[3] (optional)
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: python main.py <True|False> [person_name] [repeat]")
        sys.exit(1)

    # 1st argument: must be "True" or "False"
    hpc_arg = args[0].strip().lower()
    if hpc_arg == "true":
        on_hpc_flag = True
    elif hpc_arg == "false":
        on_hpc_flag = False
    else:
        print("Error: first argument must be True or False.")
        sys.exit(1)

    # 2nd argument: person_name (optional)
    persona = args[1] if len(args) > 1 else None

    # 3rd argument: repeat (optional, default = 2)
    if len(args) > 2:
        try:
            repeat = int(args[2])
            if repeat < 1:
                raise ValueError
        except ValueError:
            print("Error: third argument [repeat] must be a positive integer.")
            sys.exit(1)
    else:
        repeat = 3

    # Generate sizes based on whether we're on HPC
    sizes = generate_sizes(hpc=on_hpc_flag)

    # Run the comparison
    run_cron_comparison(persona, sizes, repeat)
    print("Finished run_cron_comparison() and saved results.")

