#!/bin/bash


for jobid in `squeue --me -o %A -h`; do
  echo $jobid
  eval $(scontrol show job $jobid | grep WorkDir)
  cat $WorkDir/run.py | grep "commit ="
done
