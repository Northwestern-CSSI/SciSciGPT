#!/bin/bash

conda create -n sciscigpt python=3.11 -y
conda activate sciscigpt

# install python dependencies
pip install -r requirements.txt

# install R using conda forge
conda install -c conda-forge r-essentials r-base -y
conda install rpy2 -y

# install Julia using conda forge
conda install -c conda-forge julia -y
pip install juliacall