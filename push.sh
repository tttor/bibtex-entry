#!/bin/bash

echo '=== committing ==='
git add --all
git commit -a -m add

echo '=== github.com ==='
git push origin master
