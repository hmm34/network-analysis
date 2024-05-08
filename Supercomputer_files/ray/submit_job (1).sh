#!/bin/bash
#SBATCH --job-name=my_python_job
#SBATCH --output=output.txt
#SBATCH --error=error.txt
#SBATCH --nodes=20
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=12
#SBATCH --time=15:00:00
#SBATCH --account=PWOO0021

# Load necessary modules
module load python/3.9-2022.05

# Create and activate a virtual environment (uncomment if needed)
# mkvirtualenv -p python3 myenv
# source myenv/bin/activate

# Upgrade pip in the virtual environment
pip install --upgrade pip

# Install 'wheel' package
pip install wheel

# Install Ray and other dependencies
pip install ray
# pip install networkx
# pip install matplotlib
# pip install numpy

# Display Python version
python --version


renice -n 1000 -p 123

# Run your Python script within the virtual environment
python main.py


# Deactivate the virtual environment after the job completes (uncomment if needed)
# deactivate
