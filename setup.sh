#!/bin/bash

year=$1
day=$2
if [ $day -lt 10 ]; then
    day="0$day"
fi
path="$year/Day $day"

mkdir -p "$path"

cp boilerplates/boilerplate.py "$path/test.py"
cp boilerplates/boilerplate.go "$path/pt1_2.go"
touch "$path/input.txt"