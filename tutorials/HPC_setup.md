

##  HPC Setup Instructions (VSC – Python 3.12.3 via 2024a toolchain)

### 1. Load the Python module (GCCcore 13.3.0 + Python 3.12.3)

```bash
module load Python/3.12.3-GCCcore-13.3.0
````

### 2. Confirm the Python interpreter

```bash
which python         # should point into /apps/.../2024a/software/Python/3.12.3-...
python --version     # should print "Python 3.12.3"
```

### 3. Navigate to your project folder

```bash
cd ~/cdsProject2025
```

### 4. Create and activate a virtual environment

```bash
# First-time setup (creates .venv inside the project folder)
python -m venv .venv

# Every time you start a new session
source .venv/bin/activate
```

### 5. Upgrade pip and install required packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Run the code

```bash
python kerubo_run.py

```

or

```bash
python mburu_run.py
```

