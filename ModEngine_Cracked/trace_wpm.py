import pefile
from capstone import *
from capstone.x86 import *

pe = pefile.PE(r'd:\BaiduNetdiskDownload\CheatEvolution\CheatEvolution\CheatEvolution_patched.exe')

wpm_iat = None
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    if entry.dll and (b'KERNEL32' in entry.dll.upper() or b'KERNELBASE' in entry.dll.upper()):
        for imp in entry.imports:
            if imp.name and b'WriteProcessMemory' in imp.name:
                wpm_iat = imp.address
                print(f"WriteProcessMemory IAT: {hex(wpm_iat)}")

if not wpm_iat:
    print("WriteProcessMemory not found in imports")
    exit()

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

for section in pe.sections:
    if b'.text' in section.Name:
        data = section.get_data()
        base = pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress
        
        instructions = list(md.disasm(data, base))
        for i, inst in enumerate(instructions):
            if inst.mnemonic == 'call' and inst.operands:
                op = inst.operands[0]
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    target = inst.address + inst.size + op.mem.disp
                    if target == wpm_iat:
                        print(f"\nCall to WriteProcessMemory at {hex(inst.address)}")
                        print("Previous 10 instructions:")
                        for j in range(max(0, i-10), i+1):
                            print(f"{hex(instructions[j].address)}:\t{instructions[j].mnemonic}\t{instructions[j].op_str}")

