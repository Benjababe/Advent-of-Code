param (
	[string]$year,
	[string]$day
)

$day = [string][int]$day
$day = $day | % PadLeft 2 '0'

$path = "$year\src\day_$day"

New-Item -ItemType Directory -Path $path -Force
New-Item -ItemType File -Path "$path\input.txt" -Force

Copy-Item -Path "boilerplates\boilerplate.py" -Destination "$path\test.py"
Copy-Item -Path "boilerplates\boilerplate.rs" -Destination "$path\mod.rs"

$content = Get-Content -Path "$path\mod.rs"
$newContent = $content -replace "_DAY_", $day
Set-Content -Path "$path\mod.rs" -Value $newContent