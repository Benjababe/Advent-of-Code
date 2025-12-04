param (
	[string]$year,
	[string]$day
)

$day = [string][int]$day
$day = $day | ForEach-Object PadLeft 2 '0'

$path = "$year\src\day_$day"

New-Item -ItemType Directory -Path $path -Force
New-Item -ItemType File -Path "$path\input.txt" -Force

Copy-Item -Path "boilerplates\boilerplate.py" -Destination "$path\pt1.py"
Copy-Item -Path "boilerplates\boilerplate.py" -Destination "$path\pt2.py"