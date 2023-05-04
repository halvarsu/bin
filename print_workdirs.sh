#!/bin/bash


squeue --me -o "%A %j" -h | while read -r line; do
  arrIN=(${line// / })
  jobid="${arrIN[0]}"
  jobname="${arrIN[1]}"
  echo "$jobid, $jobname"
  scontrol show job $jobid | grep WorkDir
done


# for jobid in `squeue --me -o %A -h`; do
#   echo $jobid
#   scontrol show job $jobid | grep WorkDir
# done
