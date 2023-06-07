#! /bin/sh

#SBATCH --job-name=gpt-j
#SBATCH --output=./gptj_out.txt
#SBATCH --error=./gptj_err.txt
#SBATCH --partition=killable
#SBATCH --time=1000
#SBATCH --signal=USR1@120 # how to end job when time’s up
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=50000
#SBATCH --gpus=1
#SBATCH --constraint=tesla_v100|quadro_rtx_8000

export TRANSFORMERS_CACHE=/home/joberant/home/roi1/hf_cache

python filter_benchmark_by_model.py ./benchmark/top_views_1000.json gpt-j ./benchmark/filtered/gpt-j_1000.json