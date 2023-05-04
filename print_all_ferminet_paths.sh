#!/bin/bash

# prints the path of ferminet for each conda environment

eval "$(conda shell.bash hook)"
set -f
echo "$(conda env list)" | while IFS= read -r IN; do
  IN=$(echo $IN|sed 's/\*//')
  arrIN=(${IN// / })
  if [[ $IN == \#* ]];then
    :
  else
    env_name="${arrIN[0]}"
    conda deactivate
    conda activate $env_name
    out=$( { python -c "import ferminet; print(ferminet.__path__[0])"; } 2>&1)
    if [ $? == 0 ]; then
      printf '%-40s %s' "$env_name" "$out"
    else
      printf '%-40s %s' "$env_name" "path unavailable"
    fi
    echo
  fi
done
