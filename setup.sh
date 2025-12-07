#!/bin/bash

year=$1
day=$2

day=${day#0}
if [ "$day" -lt 10 ]; then
    day="0$day"
fi

path="$year/day_$day"

mkdir -p "$path"
touch "$path/input.txt"

cp boilerplates/boilerplate.py "$path/solve.py"

# Use sed for in-place editing with compatibility for both Linux and macOS
# if [[ "$OSTYPE" == "darwin"* ]]; then
#     sed -i '' -e "s/_DAY_/$day/g" "$path/mod.rs"
# else
#     sed -i -e "s/_DAY_/$day/g" "$path/mod.rs"
# fi