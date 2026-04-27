$bytes = [System.IO.File]::ReadAllBytes('d:\BaiduNetdiskDownload\CheatEvolution\CheatEvolution\CheatEvolution_patched.exe')
$str = [System.Text.Encoding]::Unicode.GetString($bytes)
$matches = [regex]::Matches($str, '[a-zA-Z0-9_\-\.]{4,}')
$matches | Select-Object -ExpandProperty Value | Out-File "e:\CT List\ModEngine\patched_strings_unicode.txt"
