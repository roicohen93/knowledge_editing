#! /bin/sh

#SBATCH --job-name=gpt2_100
#SBATCH --output=./gptj_100_out.txt
#SBATCH --error=./gptj_100_err.txt
#SBATCH --partition=killable
#SBATCH --time=300
#SBATCH --signal=USR1@120 # how to end job when time’s up
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=50000
#SBATCH --gpus=1
#SBATCH --constraint=tesla_v100|quadro_rtx_8000

export TRANSFORMERS_CACHE=/home/joberant/home/roi1/hf_cache

python evaluation.py