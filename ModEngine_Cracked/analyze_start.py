import sys

with open(r'e:\CT List\ModEngine\startModEngine.exe', 'rb') as f:
    data = f.read()

if b'mscoree.dll' in data:
    print("Has mscoree.dll")
else:
    print("No mscoree.dll")
