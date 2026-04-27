$bytes = [System.IO.File]::ReadAllBytes('e:\CT List\ModEngine\ModEngine.exe')
$zipMagic = [byte[]](0x50, 0x4B, 0x03, 0x04)
for ($i = 0; $i -lt $bytes.Length - 4; $i++) {
    if ($bytes[$i] -eq $zipMagic[0] -and $bytes[$i+1] -eq $zipMagic[1] -and $bytes[$i+2] -eq $zipMagic[2] -and $bytes[$i+3] -eq $zipMagic[3]) {
        Write-Host "ZIP found at offset $i"
    }
}
