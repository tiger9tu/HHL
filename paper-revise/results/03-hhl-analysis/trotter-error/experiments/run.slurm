#!/bin/bash
#SBATCH --account=m5350
#SBATCH --qos=debug
#SBATCH --constraint=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128
#SBATCH --time=00:25:00
#SBATCH --job-name=hhl-trotter-bounds
#SBATCH --output=paper-revise/results/03-hhl-analysis/trotter-error/experiments/logs/slurm-%j.out
#SBATCH --error=paper-revise/results/03-hhl-analysis/trotter-error/experiments/logs/slurm-%j.err
set -euo pipefail
cd /global/u2/y/yuetu/proj/HHL
export OPENBLAS_NUM_THREADS=2
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
srun --cpu-bind=none paper-revise/results/03-hhl-analysis/trotter-error/experiments/.venv/bin/python paper-revise/results/03-hhl-analysis/trotter-error/experiments/run_experiments.py --workers 32 --resume
