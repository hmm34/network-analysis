#!/bin/bash
#SBATCH --job-name=my_python_job
#SBATCH --output=output3.txt
#SBATCH --error=error4.txt
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=28
#SBATCH --time=4:00:00
#SBATCH --account=PWOO0021

# Load necessary modules
module load python
set -x   # Enable verbose mode
# Run your Python script within the virtual environment
python main.py


echo "Completed"
