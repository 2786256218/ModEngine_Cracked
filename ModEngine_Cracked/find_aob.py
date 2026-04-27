import re

with open(r'd:\BaiduNetdiskDownload\CheatEvolution\CheatEvolution\CheatEvolution_patched.exe', 'rb') as f:
    data = f.read()

# try to find string that looks like AoB, e.g. "8B 45 ? 85 C0"
text_ascii = data.decode('ascii', errors='ignore')
matches = re.findall(r'([0-9A-Fa-f]{2} [0-9A-Fa-f\?]{1,2} [0-9A-Fa-f\? ]{5,})', text_ascii)
if matches:
    print("ASCII AoB patterns found:")
    for m in matches:
        print(m)

text_utf16 = data.decode('utf-16le', errors='ignore')
matches16 = re.findall(r'([0-9A-Fa-f]{2} [0-9A-Fa-f\?]{1,2} [0-9A-Fa-f\? ]{5,})', text_utf16)
if matches16:
    print("UTF-16 AoB patterns found:")
    for m in matches16:
        print(m)
