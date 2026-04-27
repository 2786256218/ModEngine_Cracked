$bytes = [System.IO.File]::ReadAllBytes('e:\CT List\ModEngine\ModEngine.exe')
$str = [System.Text.Encoding]::ASCII.GetString($bytes)
$matches = [regex]::Matches($str, '[a-zA-Z0-9_\-\.]{5,}')
$matches | Select-Object -First 50 -ExpandProperty Value
