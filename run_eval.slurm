#! /bin/sh

#SBATCH --job-name=gptneo
#SBATCH --output=./gptneo_out.txt
#SBATCH --error=./gptneo_err.txt
#SBATCH --partition=killable
#SBATCH --time=300
#SBATCH --signal=USR1@120 # how to end job when time’s up
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=50000
#SBATCH --gpus=1
#SBATCH --constraint=quadro_rtx_8000

export HF_HOME=/home/joberant/home/roi1/hf_cache
export TRANSFORMERS_CACHE=/home/joberant/home/roi1/hf_cache
export HF_DATASETS_CACHE=/home/joberant/home/roi1/datasets_cache

python evaluation.py