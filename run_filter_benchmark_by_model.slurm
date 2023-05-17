#! /bin/sh

#SBATCH --job-name=gpt2
#SBATCH --output=./gpt2_out.txt
#SBATCH --error=./gpt2_err.txt
#SBATCH --partition=killable
#SBATCH --time=300
#SBATCH --signal=USR1@120 # how to end job when time’s up
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=50000
#SBATCH --gpus=1
#SBATCH --constraint=tesla_v100|quadro_rtx_8000

export TRANSFORMERS_CACHE=/home/joberant/home/roi1/hf_cache

python filter_benchmark_by_model.py ./benchmark/top_views.json gpt2-medium ./benchmark/filtered/gpt2-medium.json