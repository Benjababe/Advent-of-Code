param (
	[string]$year,
	[string]$day
)

$day = [string][int]$day
$day = $day | ForEach-Object PadLeft 2 '0'

$path = "$year\day_$day"

New-Item -ItemType Directory -Path $path -Force
New-Item -ItemType File -Path "$path\input.txt" -Force

Copy-Item -Path "boilerplates\boilerplate.py" -Destination "$path\solve.py"