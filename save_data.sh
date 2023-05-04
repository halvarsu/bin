#!/bin/bash

module load Stages/2022 Python/3.9.6 CUDA/11.5 &> /dev/null

$HOME/bin/python_scripts/save_data.py "$@"
