import sys

with open(r'e:\CT List\ModEngine\ModEngine.exe', 'rb') as f:
    data = f.read()

if b'mscoree.dll' in data:
    print("Has mscoree.dll")
else:
    print("No mscoree.dll")

if b'CETRAINER' in data:
    print("Has CETRAINER")
else:
    print("No CETRAINER")

# Try to find a zip file signature (PK\x03\x04)
idx = data.find(b'PK\x03\x04')
if idx != -1:
    print(f"Zip found at offset {idx}")
else:
    print("No Zip found")

# Look for Lua scripts
idx_lua = data.find(b'function ')
if idx_lua != -1:
    print(f"Found 'function ' at {idx_lua}")

