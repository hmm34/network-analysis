# Python Supercomputer Job Starter

This repository contains a Python script intended to be run on a supercomputer using the Slurm job scheduler. The provided `submit_job.sh` script outlines the requirements and constraints for the job, and the Python script is executed within this job configuration.

## Python Script Setup

At the top of your Python script, include the following shebang line to specify the Python interpreter:

#!/usr/bin/env python

This ensures that the script is executed using the Python interpreter specified in the user's environment.


## Slurm Job Configuration (submit_job.sh)

Create a Slurm job configuration script named `submit_job.sh` with the following content:

#!/bin/bash
#SBATCH --job-name=my_python_job       # Specify the name of the job
#SBATCH --output=output.txt            # Specify the output file for the job
#SBATCH --error=error.txt              # Specify the error file for the job
#SBATCH --nodes=1                      # Specify the number of nodes to be used
#SBATCH --ntasks-per-node=1            # Specify the number of tasks per node
#SBATCH --cpus-per-task=4              # Specify the number of CPUs to use for each task
#SBATCH --time=01:00:00                # Specify the duration of the job (hours:minutes:seconds)
#SBATCH --account=your_account_name    # Replace 'your_account_name' with the project ID

module load python                     # Load the Python module if needed
python my_script.py                    # Specify the Python script to be executed


## Running the Job

To submit the job, open the command line by clicking the "Open in Terminal" button in the file directory and enter the following command:
 
sbatch submit_job.sh

This command submits the job to the Slurm scheduler, and the output and error messages will be recorded in the specified files (`output.txt` and `error.txt`, respectively). Adjust the parameters in `submit_job.sh` to suit the specific requirements of your Python script and job.


## UNFINISHED WORK:
- The directory called Ray contains the implementation for the computation of the alpha-i-metric of a graph using Ray for parallel processing.
As it is right now, the ray aspect of this program keeps giving errors that indicate that the ray intances/threads are being killed off because
of insufficient memory.

- The directory called multiprocessing contains the implementation for the computation of the alpha-i-metric of a graph using Ray for parallel processing.
As it is right now, this aspect can produces the alpha-i-metric for really small graphs like the one in social.txt, but for some reason, halts (whilst still being an active job)
itself with no error/ output message after 40 minutes of the function running.

