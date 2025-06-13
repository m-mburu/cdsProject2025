Project Concepts of Data Science 2024-2025
================

Students:

- **Anita Kerubo \[2469491\]**
- **Moses Mburu \[2469245\]**

## Project Structure

This project implements a benchmarking framework for comparing a Ternary
Search Tree (TST) and a B-tree. Below are the key files and directories:

### Core Scripts

#### [`main.py`](./main.py)

This is the main script that runs all our experiments comparing two tree
data structures:

- **TSTree** (Ternary Search Tree – the one we built)
- **Btree** (Binary Search Tree – as explained in lectures)

##### Steps the script performs:

1.  **Chooses dataset sizes** based on where you run the script:

    - If running locally: sizes go up to 15,000
    - If running on an HPC system: sizes go up to 50,000
    - The sizes are spaced out in 10 steps (like 5,000 → 10,000 → … →
      50,000)

2.  **Runs benchmarks** on three types of test cases:

    - Best case: words with shared prefixes (like “apple”, “apply”,
      “app”)
    - Average case: completely random words
    - Worst case: progressive words (like “a”, “aa”, “aaa”, …)

3.  **Measures how long it takes** to insert and search using each tree
    type for all cases and dataset sizes.

4.  **Repeats each test several times** (default is 5) to get more
    reliable results.

5.  **Saves the results** as a CSV file:

    - If you give your name, it saves as `data/df_<yourname>.csv`
    - If not, it saves as `data/df.csv`

6.  **Example usage from the command line:**

``` bash
python main.py True moses 5
```

This tells the script:

- You are running it on HPC (`True`)
- Your name is Moses
- Repeat each test 5 times

##### Output folder

The results are saved in the `data/` folder. This folder is created
automatically if it doesn’t exist. You can use the CSV file for further
analysis or plotting.

#### [`requirements.txt`](./requirements.txt)

This file lists all the Python packages our project needs to run.

- We use **`pandas`** to handle and save our benchmark results (like
  working with Excel or tables).
- We use **`psutil`** to measure how much memory (RAM) our program uses
  during testing.

This file helps make sure that **everyone runs the project with the same
tools**, especially on shared systems like the HPC.

After you turn on your Python environment, just run:

``` bash
pip install -r requirements.txt
```

This will install everything you need to run the project.

#### [`tstree.py`](./src/tstree/tstree.py)

This is the main tree we built and tested in our project, to compare
against the Binary Search Tree from class.

- Each node stores **one character**

- It can link to:

  - a **left child** for smaller characters,
  - a **middle child** for the next letter in the word,
  - and a **right child** for bigger characters.

#### methods implemented

- **Insert** new words.
- **Search** for exact matches.
- **List all stored words**.
- **Print a tree structure**, to help you see how it looks.

#### [`btree.py`](./src/btree/btree.py)

This file contains the **`Btree` class**, a **Binary Search Tree (BST)**
implementation based on the version taught in our **course lectures**.

- Each node holds a **full word**.

- It has:

  - a **left child** for words that come before it alphabetically,
  - a **right child** for words that come after.

We use this as a **reference implementation** to compare against our
`TSTree` (Ternary Search Tree).

This helps us show where the TSTree performs better or worse than the
standard BST from class.

### Testing & Experiments

#### [`benchmark.py`](./src/benchmark/benchmark.py)

This file contains the core functions for **testing how well our tree
structures perform**.

1.  **Creates different types of word lists** for testing:

    - **Best case** – words with the same starting letters
      (e.g. “apple”, “apply”, “appoint”). This is good for TSTs because
      they reuse the prefix.
    - **Worst case** – words like “a”, “aa”, “aaa”, …, which are known
      to break BST performance.
    - **Average case** – randomly generated words with no special
      pattern.

2.  **Measures performance for each tree**:

    - How long it takes to insert the words into the tree.
    - How long it takes to search for all the words in the tree.
    - How much memory (RAM) the tree uses after inserting the words.

3.  **Repeats each test several times** to reduce random variation and
    calculate averages.

4.  **Supports multiple trees**:

    - Runs the same tests on both `TSTree` and `Btree`.

    - Saves the results for each tree in columns like:

      - `tst_insert`, `tst_search`, `tst_ram`
      - `bst_insert`, `bst_search`, `bst_ram`

5.  You can choose:

    - The **number of words** to test with (dataset size).
    - The **type of test case** (best, worst, or average).
    - The **number of repetitions** for averaging.

If you test `TSTree` and `Btree` with 10,000 random words:

- It inserts all 10,000 words into each tree.
- It searches for all 10,000 words.
- It measures how much time and memory each tree uses.
- It repeats this 5 times.
- It returns the average results in a DataFrame.

That DataFrame is then saved to CSV by the `main.py` script.

#### [`plot_functions.py`](./src/benchmark/plot_functions.py)

This file defines a function to **plot benchmark results**.

It takes the output DataFrame from the benchmarking script and helps you
**visualize how each tree performs** across different cases (best,
worst, average) and sizes.

1.  **Reads your benchmark results** – it expects columns like `size`,
    `case`, and the actual performance metrics (e.g. `tst_insert`,
    `bst_ram`).

2.  **Reshapes the data** it turns wide columns into long format for
    Seaborn plotting.

3.  **Separates the metric column** into two parts:

    - the **tree type** (e.g. `tst` or `bst`)
    - the **test type** (e.g. `insert`, `search`, or `ram`)

4.  **Draws a line plot** using Seaborn’s `relplot()`:

    - x-axis: number of words (`size`)
    - y-axis: performance (time or RAM)
    - separate plots (facets) for each test type
    - different lines for each case (best, worst, average)

5.  Returns plot

#### [bench.slurm](./bench.slurm)

This is the SLURM job script we used to run our benchmarking tests on
the HPC. It requests the needed resources, loads the required Python
module, sets up and activates a virtual environment, installs any
missing packages, and then runs `main.py` in HPC mode. It also saves
logs to the `logs/` folder and sends email notifications to both group
members.

### Data Files

#### - [Data files from runs](./data)

Since this was a team project, we decided to save our benchmark results
using our names.

The `data/` folder contains CSV files from our tests:

- `df_anita.csv` for Anita’s runs
- `df_moses.csv` for Moses’ runs

Each file stores the results of benchmarking the `TSTree` and `Btree`
structures on different dataset sizes, tested under **best**, **worst**,
and **average** cases.

The data includes:

- Time to insert
- Time to search
- Memory used

### Documentation

#### - [`README.md`](./README.md)

We wrote our README using [**RMarkdown**](./README.rmd) , since it gives
us more flexibility to include **text, plots, and code** in one place.
It enables to directly knit directly to `.md` `github_document` format.

#### - [`HPC_setup.md`](./tutorials/HPC_setup.md)

This file is a guide that explains how to set up your Python environment
and run the benchmark script on the HPC system.

#### - [`SLURM.md`](./tutorials/SLURM.md)

This file explains how to write and submit a SLURM job script to run the
benchmark on an HPC system. It shows how to request resources, load
modules, activate your environment, and run the script. It also includes
tips for logging, setting your email, and tracking job progress.

- [`docs/project_2024_2025.docx`](./docs/project_2024_2025.docx)

  The `docs/project_2024_2025.docx` is the assignment file

You can run any of the benchmark scripts using:

``` bash
python main.py <True|False> [person_name]
```

- where `<True|False>` indicates whether to run on HPC, and
  `[person_name]` is an optional argument to specify the contributor’s
  name for output file naming. This will generate a CSV file in the
  `data/` directory with the results of the benchmark tests.

### Results

``` python
import pandas as pd
## load all the data in a for loop from data/ 
import os
data_dir = "data/"
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
data_frames = {}
data_frames_list = []
for file in files:
    file_path = os.path.join(data_dir, file)
    print(f"Loading {file_path}")
    df = pd.read_csv(file_path)
    data_frames[file] = df
    data_frames_list.append(df)
```

    ## Loading data/df_moses.csv
    ## Loading data/df_anita.csv

``` python
## print the names of the data frames
# print("Data frames loaded:")
# for name in data_frames.keys():
#     print(name)

df = pd.concat(data_frames_list, ignore_index=True)
```

#### Summary Statistics

We compared how fast and memory-efficient `TSTree` and `Btree` are
across different input cases—**best**, **average**, and **worst**.

``` python
# Melt the dataframe to long format
melted_df = df.melt(
    id_vars=["case", "size"],
    value_vars=[col for col in df.columns if col.startswith(("tst_", "bst_"))],
    var_name="metric",
    value_name="value"
)


melted_df["tree_type"] = melted_df["metric"].str.extract(r'^(tst|bst)')

melted_df["metric"] = melted_df["metric"].str.extract(r'^[a-z]+_(.*)$')

summary_stats = melted_df.groupby(["case", "tree_type", "metric"]).value.describe().round(3).reset_index()
print(summary_stats.to_markdown(index=False)) # install tabulate to use this function
```

    ## | case    | tree_type   | metric   |   count |    mean |     std |   min |   25% |   50% |     75% |      max |
    ## |:--------|:------------|:---------|--------:|--------:|--------:|------:|------:|------:|--------:|---------:|
    ## | average | bst         | insert   |      20 |   0.025 |   0.03  | 0     | 0.004 | 0.007 |   0.045 |    0.1   |
    ## | average | bst         | ram      |      20 |   0     |   0     | 0     | 0     | 0     |   0     |    0     |
    ## | average | bst         | search   |      20 |   0.016 |   0.02  | 0     | 0.003 | 0.005 |   0.027 |    0.065 |
    ## | average | tst         | insert   |      20 |   0.119 |   0.141 | 0.001 | 0.018 | 0.04  |   0.23  |    0.407 |
    ## | average | tst         | ram      |      20 |   2.627 |   3.633 | 0     | 0     | 0.466 |   5.119 |   11.685 |
    ## | average | tst         | search   |      20 |   0.034 |   0.04  | 0.001 | 0.006 | 0.013 |   0.063 |    0.127 |
    ## | best    | bst         | insert   |      20 |   0.018 |   0.02  | 0     | 0.003 | 0.007 |   0.027 |    0.068 |
    ## | best    | bst         | ram      |      20 |   0.018 |   0.034 | 0     | 0     | 0     |   0.009 |    0.108 |
    ## | best    | bst         | search   |      20 |   0.011 |   0.012 | 0     | 0.002 | 0.003 |   0.017 |    0.038 |
    ## | best    | tst         | insert   |      20 |   0.033 |   0.037 | 0.001 | 0.006 | 0.013 |   0.054 |    0.115 |
    ## | best    | tst         | ram      |      20 |   0.181 |   0.179 | 0     | 0.036 | 0.126 |   0.29  |    0.551 |
    ## | best    | tst         | search   |      20 |   0.021 |   0.024 | 0.001 | 0.004 | 0.007 |   0.035 |    0.075 |
    ## | worst   | bst         | insert   |      20 | 223.552 | 410.988 | 0.013 | 0.583 | 2.053 | 223.288 | 1424.63  |
    ## | worst   | bst         | ram      |      20 |   0.074 |   0.065 | 0     | 0.023 | 0.07  |   0.108 |    0.22  |
    ## | worst   | bst         | search   |      20 | 188.603 | 343.924 | 0.011 | 0.49  | 1.613 | 194.091 | 1187.9   |
    ## | worst   | tst         | insert   |      20 |  41.078 |  65.158 | 0.02  | 0.779 | 2.25  |  56.053 |  207.884 |
    ## | worst   | tst         | ram      |      20 |   0.276 |   0.238 | 0     | 0.139 | 0.19  |   0.382 |    1.005 |
    ## | worst   | tst         | search   |      20 |  40.528 |  64.167 | 0.021 | 0.75  | 2.264 |  55.173 |  204.275 |

#### Plots

``` python
from src.benchmark.plot_functions import plot_facet_metrics
import matplotlib.pyplot as plt

for name, df in data_frames.items():
    clean_name = os.path.splitext(name)[0]
    print(f"Plotting metrics for {clean_name}")
    
    # First, check if required columns exist
    if 'size' in df.columns:
        # If 'case' column doesn't exist, try to add it using the filename
        if 'case' not in df.columns:
            df['case'] = clean_name  # Add file identifier as 'case'
            
        try:
            # Use default id_vars
            g = plot_facet_metrics(df)
            plt.suptitle(f"Metrics for {clean_name}")
            plt.tight_layout()
            plt.show()  # Force display of current plot before creating next one
        except Exception as e:
            print(f"Error plotting {clean_name}: {e}")
    else:
        print(f"DataFrame {clean_name} lacks required 'size' column")
```

<img src="README_files/figure-gfm/unnamed-chunk-3-1.png" width="1451" /><img src="README_files/figure-gfm/unnamed-chunk-3-2.png" width="1451" />

``` python
best_bst_ins   = summary_stats.query("case=='best'   & tree_type=='bst' & metric=='insert'")["mean"]
best_bst_srch  =  summary_stats.query("case=='best'   & tree_type=='bst' & metric=='search'")["mean"]
best_tst_ins   =  summary_stats.query("case=='best'   & tree_type=='tst' & metric=='insert'")["mean"]
best_tst_srch  =  summary_stats.query("case=='best'   & tree_type=='tst' & metric=='search'")["mean"]

avg_bst_ins    =  summary_stats.query("case=='average' & tree_type=='bst' & metric=='insert'")["mean"]
avg_tst_ins    =  summary_stats.query("case=='average' & tree_type=='tst' & metric=='insert'")["mean"]
avg_bst_srch   =  summary_stats.query("case=='average' & tree_type=='bst' & metric=='search'")["mean"]
avg_tst_srch   =  summary_stats.query("case=='average' & tree_type=='tst' & metric=='search'")["mean"]

worst_bst_ins  =  summary_stats.query("case=='worst'  & tree_type=='bst' & metric=='insert'")["mean"]
worst_bst_srch =  summary_stats.query("case=='worst'  & tree_type=='bst' & metric=='search'")["mean"]
worst_tst_ins  =  summary_stats.query("case=='worst'  & tree_type=='tst' & metric=='insert'")["mean"]
worst_tst_srch =  summary_stats.query("case=='worst'  & tree_type=='tst' & metric=='search'")["mean"]
```

##### Insert and Search Time

- In the **best case** both trees were fast, but `Btree` was faster.

  - `Btree`: insert $\approx$ 0.018 s, search $\approx$ 0.011 s  
  - `TSTree`: insert $\approx$ 0.033 s, search $\approx$ 0.021 s

- In the **average case** the gap grows.

  - `Btree`: insert $\approx$ 0.025 s, search $\approx$ 0.016 s
  - `TSTree`: insert $\approx$ 0.119 s, search $\approx$ 0.034 s  
    so `TSTree` was about **0.2×** slower here.

- In the **worst case** the difference is huge.

  - `Btree`: insert $\approx$ 224 s, search $\approx$ 189 s  
  - `TSTree`: insert $\approx$ 41 s, search $\approx$ 41 s  
    so `TSTree` was about **5.4×** faster here.

This shows that `TSTree` handles bad cases much better than `Btree`,
especially when words share long prefixes.

##### Memory Use

- `Btree` used almost no memory in best and average cases.

- `TSTree` used more memory throughout:

  - Average case: $\approx$ 4.88 MB
  - Worst case: $\approx$ 0.41 MB

Even though `TSTree` used more RAM, it stayed within reasonable limits.

### Conclusion

- `Btree` is **very fast** and **lightweight** when input is random or
  sorted alphabetically.
- `TSTree` is **slightly slower** in simple cases, but much **faster and
  more stable** in worst-case scenarios (e.g., when words are nested
  like `"a"`, `"aa"`, `"aaa"`, …).
- So if you expect structured or repetitive input, `TSTree` is the
  better choice. Otherwise, `Btree` is fine and faster.

These results match what we see in the plots—`TSTree` grows more
steadily while `Btree` slows down a lot as size increases under bad
inputs.

### References

- [Top coder tst
  trees](https://www.topcoder.com/thrive/articles/ternary-search-trees#:~:text=Ternary%20search%20trees%20are%20a,consumes%20a%20lot%20of%20memory)

- <https://en.wikipedia.org/wiki/Ternary_search_tree>
