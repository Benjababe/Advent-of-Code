@echo off
set year=%1
set day=%2
if %day% LSS 10 set day=0%day%
set path="%year%\Day %day%"

mkdir %path%
copy boilerplates\boilerplate.py %path%\test.py
copy boilerplates\boilerplate.go %path%\pt1_2.go
echo. > %path%\input.txt
