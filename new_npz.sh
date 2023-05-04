#!/bin/bash

module load Stages/2020 Python/3.8.5  &> /dev/null

python $HOME/bin/new_npz.py "$@"
