# SLURM Job Submission on HPC: Step-by-Step Guide

## Introduction

This guide outlines the process of creating and running a SLURM job script on a High-Performance Computing (HPC) system, based on real troubleshooting experience. It includes useful commands and practical tips to avoid common pitfalls.

A `.slurm` file is a bash script with SLURM directives that tell HPC scheduler how to allocate resources and what job to run.

### Breakdown of Key Directives

| Line                          | What it Does                                        |
| ----------------------------- | --------------------------------------------------- |
| `#!/bin/bash`                 | Tells the system this is a bash script              |
| `#SBATCH --job-name=...`      | A name to identify your job                         |
| `#SBATCH --output=...`        | File to save output log                             |
| `#SBATCH --time=...`          | Max wall clock time your job can run                |
| `#SBATCH --cpus-per-task=...` | Number of CPU cores to use                          |
| `#SBATCH --mem=...`           | How much memory you request                         |
| `module load ...`             | Loads the Python module (version depends on system) |
| `source ~/myenv/bin/activate` | Activates your Python virtual environment           |
| `python <your_script.py>`       | Runs your actual benchmark code                     |


## 1. Create Your SLURM Script

* **SSH into the login node** of your HPC.

* `cd` to the project directory.

* Create a new .slurm file in your project folder (e.g. *run_benchmark.slurm*). Add the following structure and customize it as needed:

```bash
#!/bin/bash
#SBATCH --job-name=benchmark_test         # Name of your job
#SBATCH --output=logs/output_%j.log       # Output log path (create logs folder first)
#SBATCH --error=logs/error_%j.log         # Error log path (create logs folder first)
#SBATCH --time=01:00:00                   # Max walltime (HH:MM:SS)
#SBATCH --cpus-per-task=4                 # Number of CPU cores
#SBATCH --mem=16G                         # Memory required
#SBATCH --mail-type=END,FAIL              # Get email for end/failure
#SBATCH --mail-user=your.email@domain.com # Your email address
#SBATCH -A lp_h_ds_students               # Account to charge job to. (Adjust if different)
#SBATCH -M genius                         # Cluster name (e.g. genius or wice) 
#SBATCH --partition=genius_batch          # Valid partition name for that cluster

```

Tips:

+ **Job name:** Choose something meaningful.

+ `%j` in the **output/error** file path gets replaced automatically by the job ID once you submit the slurm script.

+ Create the **logs folder** before running the job: `mkdir -p <your-project-file-path>/logs`

+ Use your **actual email address** to receive notifications.

+ Use the **correct account name** shown by: `sacctmgr show user $(whoami) withassoc`

+ Find available **clusters** using `module spider Python/...` or log in to the HPC via shell.

+ Use `sinfo -M <cluster>` to **list partitions** for a given cluster.


## 2. Load Required Modules

After setting up the SLURM header, the body of the script should load the necessary modules:

```bash
module purge
module load cluster/genius/batch      # Load the environment for your cluster
module load Python/3.11.5-GCCcore-13.2.0  # You can load a different python version
```

> ❗ If you see errors about unavailable modules or extensions, check with: 
> `module spider Python/3.11.5-GCCcore-13.2.0`. 
> This tells you which environments you must load first (like `cluster/genius/batch`).


## 3. Set Up Python Environment

Create and activate a virtual environment:

```bash
python -m venv myenv
```

* Use `which python` to get the absolute path to your Python binary. Then activate the environment in your SLURM script using that absolute path (slightly adjusted):

```bash
source /vsc-hard-mounts/leuven-user/your_folder_path/myenv/bin/activate
```

* Install your dependencies: [Tip: Always **activate your virtual environment** before running the command below, so dependencies install in the right location.]

```bash
pip install -r requirements.txt
```

A `requirements.txt` file is a plain text file that **lists all the Python packages your project needs to run**. It ensures your code runs with the correct versions of libraries — especially important when working in shared environments like HPC.

* You can check the Python version in your virtual environment:

```bash
python --version
```


## 4. Finalize Script to Run Your Code

At the end of the SLURM script, **activate the environment and run your script**:

```bash
source /vsc-hard-mounts/leuven-user/your_folder_path/myenv/bin/activate
python python <path/to/your/main-entry-point-file>.py
```

Replace `<path/to/your/main-entry-point-file>.py` with the actual path and filename of your script — this is the Python file that starts your project, runs your benchmark, or launches the core functionality.


## 5. Submit and Monitor the Job

* Submit the job:

```bash
sbatch run_benchmark.slurm
```

* If submission succeeds SLURM echoes something like:

```
Submitted batch job **1234567**
```

* Monitor job status:

```bash
squeue -u $(whoami)        # View running jobs
sacct -j <jobid>           # Replace <jobid> to see job details
```

## Debugging and Common Errors

| Error Message (abridged)                                               | Likely Cause                                        | Quick Fix                                                                                                                    |
| :--------------------------------------------------------------------- | :-------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `Please select a cluster via -M`                                       | No cluster specified                                | Add `#SBATCH -M <cluster>` or `sbatch -M <cluster>`                                                                          |
| `Please select a credit account via -A`                                | No project/account                                  | Add `#SBATCH -A <account>` (see `sacctmgr show user $(whoami) withassoc`)                                                    |
| `invalid partition specified`                                          | Partition doesn’t exist on the chosen cluster       | Replace `--partition=` with a valid one (`sinfo -M <cluster>`)                                                               |
| `module exists but cannot be loaded`<br/>`libpython3.12.so… not found` | Module hierarchy not loaded or wrong Python version | 1) `module load cluster/<cluster>/<partition>` first<br/>2) Load a Python version that really exists (`module avail Python`) |
| `ImportError: cannot import name 'Literal'`                            | Using too-old Python for modern code                | Load / install Python ≥ 3.8 (Literal added in 3.8)                                                                           |

