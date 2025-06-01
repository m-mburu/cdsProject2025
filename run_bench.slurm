#!/bin/bash
#SBATCH --job-name=kerubo-tst-benchmark                    # Job name
#SBATCH --output=cdsProject2025/logs/output_%j.log         # Output log (%j = job ID)
#SBATCH --error=cdsProject2025/logs/error_%j.log           # Error log
#SBATCH --time=02:00:00                                    # Max runtime
#SBATCH --partition=batch                                  # Adjust if needed
#SBATCH --nodes=1                                          # One node
#SBATCH --ntasks=1                                         # One task (single job)
#SBATCH --cpus-per-task=4                                  # 4 CPU cores
#SBATCH --mem=8G                                           # Memory allocation
#SBATCH --mail-type=END,FAIL                               # Email notifications
#SBATCH --mail-user=anita.ogero@student.uhasselt.be        # Replace with your email
#SBATCH -M genius                                          # Explicitly state the cluster
#SBATCH -A lp_h_ds_students                                # Add your real account here

# Optional: If you need MPI in the future, uncomment
# module load OpenMPI

# Optional: If you want to use GUI tools/X11 forwarding (e.g., matplotlib with GUI), uncomment
# module load X11

module purge
module load cluster/genius/batch

# Load Python module (adjust version if needed)
module load Python/3.12.3-GCCcore-13.3.0

# Activate your virtual environment
source /vsc-hard-mounts/leuven-user/374/vsc37481/myenv/bin/activate

# Run the main script
python cdsProject2025/main.py True "$USER" 5
