#!/bin/bash
# git remote add originbitbucket git@bitbucket.org:tttor/bibtex-entry.git
# git remote add origin git@gitlab.com:tttor/bibtex-entry.git
# https://askubuntu.com/questions/370697/how-to-count-number-of-files-in-a-directory-but-not-recursively

echo '=== n entries ==='
find ./entry -maxdepth 1 -type f | wc -l

echo '=== committing ==='
git add --all
git commit -a -m add

echo '=== github.com ==='
git push origin master

echo '=== bitbucket.org ==='
git push originbitbucket master

echo '=== bitbucket.org ==='
git push origingitlab master
