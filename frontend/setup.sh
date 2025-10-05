#!/bin/bash

conda activate sciscigpt
conda install -c conda-forge nodejs -y
conda install -c conda-forge pnpm -y
pnpm install
