#!/bin/bash

cd "2018" || exit

for dir in */ ; do
  if [ -d "$dir" ]; then
    match_found=0
    for file in "$dir"*; do
      if [[ -f "$file" && "$file" =~ $*full\.txt ]]; then
        match_found=1
        break
      else
        missing=$file
      fi
    done

    if [ $match_found -eq 1 ]; then
      echo "yes"
    else
      echo "no: $missing"
    fi
  fi
done
