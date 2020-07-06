#!/bin/bash
# git remote add originbitbucket git@bitbucket.org:tttor/bibtex-entry.git

echo '=== committing ==='
git add --all
git commit -a -m add

echo '=== github.com ==='
git push origin master

echo '=== bitbucket.org ==='
git push originbitbucket master
