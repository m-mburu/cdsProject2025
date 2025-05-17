import random
import os
import pandas as pd
import sys

#from Assignments.assignment1 import dna_match, collect_email_from_text
from src.tstree.tstree import TSTree
from src.btree.btree import Btree
from src.benchmark.benchmark import run_comparison
from typing import List

def run_cron_comparison(person_name, sizes, repeat):
    """
    Runs the comparison and saves the results to a CSV file.

    Args:
        person_name (str): The name of the person running the comparison.
        sizes (list): A list of sizes to use for the comparison.
        repeat (int): The number of times to repeat the comparison.
    """
    random.seed(100)
    
    df_best = run_comparison(sizes, tree_specs=[("tst", TSTree)], repeat=repeat, case="best")
    df_worst = run_comparison(sizes, tree_specs=[("tst", TSTree)], repeat=repeat, case="worst")
    df_average = run_comparison(sizes, tree_specs=[("tst", TSTree)], repeat=repeat, case="average")
    
    # Combine results
    df = pd.concat([df_best, df_worst, df_average], keys=["best", "worst", "average"], names=["case"])
    
    # Save DataFrame to data/ directory with person's name
    os.makedirs("data", exist_ok=True)
    filename = f"data/df_{person_name.lower()}.csv"
    df.to_csv(filename, index=True)
    print(f"Saved results to {filename}")
    print(df)



def generate_sizes(hpc: bool = False,
                   max_n: int | None = None) -> List[int]:
    """
    Return a list of dataset sizes for benchmarking.
    
    Parameters
    ----------
    hpc : bool, default False
        • False  → sizes span 1e4 … 5e5  (quick local runs)  
        • True   → sizes start at 1e6 and grow up to `max_n`
    max_n : int, optional
        Only used when `hpc=True`.  Hard upper bound for the sequence.
        Defaults to 5_000_000 (5 M).

    """
    if not hpc:
        # q
        return [10_000, 50_000, 100_000, 250_000, 500_000]

    # HPC grid
    if max_n is None:
        max_n = 5_000_000

    sizes, n, factor = [], 1_000_000, 2.0
    while n <= max_n:
        sizes.append(n)
        # a
        factor = 2.5 if factor == 2.0 else 2.0
        n = int(n * factor)

    return sizes
