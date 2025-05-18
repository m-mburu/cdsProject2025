#!/bin/bash

set -e  # Stop script if any command fails

echo "Starting Python environment setup..."

# Step 1: Download and install Miniconda (if not already installed)
if [ ! -d "$HOME/miniconda" ]; then
    echo "Downloading Miniconda installer..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

    echo "Installing Miniconda to $HOME/miniconda..."
    bash miniconda.sh -b -p "$HOME/miniconda"

    echo "Initializing Conda..."
    eval "$($HOME/miniconda/bin/conda shell.bash hook)"
    conda init

    echo "Miniconda installation complete. Please restart your shell or run: source ~/.bashrc"
else
    echo "Miniconda already installed at $HOME/miniconda"
    eval "$($HOME/miniconda/bin/conda shell.bash hook)"
fi

# Step 2: Create Conda environment if it doesn't exist
if ! conda info --envs | grep -q "^pyenv"; then
    echo "Creating Conda environment 'pyenv' with Python 3.14..."
    conda create -n pyenv python=3.14 -y
else
    echo "Environment 'pyenv' already exists."
fi

# Step 3: Activate environment and install packages
echo "Activating 'pyenv'..."
conda activate pyenv


echo "Setup complete!"
