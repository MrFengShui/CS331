#!/bin/sh
for mode in "bfs" "dfs" "iddfs" "astar"
do
    for num in 1 2 3
    do
        python hw1.py start$num.txt goal$num.txt $mode output-$mode-$num.txt
    done
done
