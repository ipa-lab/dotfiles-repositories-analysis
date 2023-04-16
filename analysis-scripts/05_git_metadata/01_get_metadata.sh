#!/bin/bash

folder_name=$1
TZ=UTC

echo -n $folder_name,

cd $folder_name
last_commit=$(git log --all -n1 --date=iso-local | grep "^Date:" | sed -n -e "1,1{s/Date:\s*//;s/\s*+.*$//;p}")
first_commit=$(git log --all --reverse --date=iso-local | sed -n -e "3,3{s/Date:\s*//;s/\s*+.*$//;p}")
number_commits=$(git rev-list --all --count)

[[ "$number_commits" > 0 ]] && approx_authors=$(git shortlog --all -sen | wc -l) || approx_authors=0

cd - >/dev/null

echo $first_commit,$last_commit,$number_commits,$approx_authors