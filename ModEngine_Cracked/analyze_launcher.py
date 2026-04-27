import sys
import re

with open(r'd:\BaiduNetdiskDownload\CheatEvolution\CheatEvolution\Launcher.exe', 'rb') as f:
    data = f.read()

# Let's check some common signatures
if b'PyInstaller' in data or b'MEI\0\0' in data:
    print("PyInstaller")
if b'AutoHotkey' in data:
    print("AutoHotkey")
if b'Go build' in data:
    print("Go binary")
if b'Electron' in data:
    print("Electron")
if b'Lazarus' in data:
    print("Lazarus/Delphi")

# Print first 50 ascii strings
text_ascii = data.decode('ascii', errors='ignore')
matches = re.findall(r'([a-zA-Z0-9_\-\.]{5,})', text_ascii)
print(matches[:50])

