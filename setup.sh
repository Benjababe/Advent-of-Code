#!/bin/bash

year=$1
day=$2

if [ $day -lt 10 ]; then
    day="0$day"
fi

path="$year/src/day_$day"

mkdir -p "$path"
touch "$path/input.txt"

cp boilerplates/boilerplate.py "$path/test.py"
cp boilerplates/boilerplate.rs "$path/mod.rs"

sed -i '' -e "s/_DAY_/$day/g" "$path/mod.rs"