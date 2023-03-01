#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=ami100
#SBATCH --output=sample-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=dasr8731@colorado.edu

module purge

module load conda 
module load cuda 
module load cudnn

cd /scratch/alpine/dasr8731/semantic-search/ 
conda load gpuenv 

python3 -m src.data_processing.get_embeddings


