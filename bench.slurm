#!/bin/bash
#SBATCH --job-name=bench_tst
#SBATCH --output=logs/%x_%j.out     # %x = job-name
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=2
#SBATCH --clusters=genius
#SBATCH --partition=batch
#SBATCH --account=lp_h_ds_students   # <-- your valid credit account
#SBATCH --mail-user=anita.ogero@student.uhasselt.be,moses.mburu@student.uhasselt.be


# -----------------------------------------------------------------
# 1. Load required modules
# -----------------------------------------------------------------
module purge
module load cluster/genius/batch
module load Python/3.11.5-GCCcore-13.2.0

# -----------------------------------------------------------------
# 2. Define your project directory (using $USER)
# -----------------------------------------------------------------
PROJECT_DIR="/vsc-hard-mounts/leuven-user/374/$USER/cdsProject2025"

# -----------------------------------------------------------------
# 3. Change into your project directory
# -----------------------------------------------------------------
cd "$PROJECT_DIR" || { echo "ERROR: cannot cd to $PROJECT_DIR"; exit 1; }

# -----------------------------------------------------------------
# 4. Create a virtual environment if it doesn’t exist
# -----------------------------------------------------------------
VENV_DIR="$PROJECT_DIR/myenv"
if [ ! -d "$VENV_DIR" ]; then
    python -m venv "$VENV_DIR"
fi

# -----------------------------------------------------------------
# 5. Activate the virtual environment
# -----------------------------------------------------------------
source "$VENV_DIR/bin/activate"

# -----------------------------------------------------------------
# 6. Install/upgrade dependencies
# -----------------------------------------------------------------
pip install --upgrade pip
pip install -r requirements.txt

# -----------------------------------------------------------------
# 7. Run main.py:
#    1st arg: True|False (HPC mode)
#    2nd arg: $USER (login name)
#    3rd arg: repeat count (e.g. 5)
# -----------------------------------------------------------------
python main.py True "$USER" 5

# -----------------------------------------------------------------
# 8. Deactivate the virtual environment
# -----------------------------------------------------------------
deactivate
