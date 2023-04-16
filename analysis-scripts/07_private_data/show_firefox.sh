#!/bin/bash

cd repos*/$1
echo Now at $(pwd)
git checkout $3
~/tools/firefox_decrypt/firefox_decrypt.py ${2//logins.json/} | less
git checkout -


# Usage:
# for line in $(cat /tmp/logins_paths) ; do (echo $line | sed 's/,/ /g' | xargs bash dotfiles-analyse/07_private_data/show_firefox.sh) ; done