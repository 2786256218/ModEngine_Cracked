import ctypes
import ctypes.wintypes
import sys
import struct
import time
import subprocess

kernel32 = ctypes.windll.kernel32

# Debug constants
DEBUG_PROCESS = 0x00000001
DEBUG_ONLY_THIS_PROCESS = 0x00000002
CREATE_NEW_CONSOLE = 0x00000010

class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.wintypes.DWORD),
        ("lpReserved", ctypes.wintypes.LPWSTR),
        ("lpDesktop", ctypes.wintypes.LPWSTR),
        ("lpTitle", ctypes.wintypes.LPWSTR),
        ("dwX", ctypes.wintypes.DWORD),
        ("dwY", ctypes.wintypes.DWORD),
        ("dwXSize", ctypes.wintypes.DWORD),
        ("dwYSize", ctypes.wintypes.DWORD),
        ("dwXCountChars", ctypes.wintypes.DWORD),
        ("dwYCountChars", ctypes.wintypes.DWORD),
        ("dwFillAttribute", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("wShowWindow", ctypes.wintypes.WORD),
        ("cbReserved2", ctypes.wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.wintypes.BYTE)),
        ("hStdInput", ctypes.wintypes.HANDLE),
        ("hStdOutput", ctypes.wintypes.HANDLE),
        ("hStdError", ctypes.wintypes.HANDLE),
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", ctypes.wintypes.HANDLE),
        ("hThread", ctypes.wintypes.HANDLE),
        ("dwProcessId", ctypes.wintypes.DWORD),
        ("dwThreadId", ctypes.wintypes.DWORD),
    ]

class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [
        ("dwDebugEventCode", ctypes.wintypes.DWORD),
        ("dwProcessId", ctypes.wintypes.DWORD),
        ("dwThreadId", ctypes.wintypes.DWORD),
        ("u", ctypes.c_byte * 160), # union padding
    ]

si = STARTUPINFO()
si.cb = ctypes.sizeof(si)
pi = PROCESS_INFORMATION()

# Start CheatEvolution so the patcher can find it
print("Starting CheatEvolution.exe...")
ce_proc = subprocess.Popen([r'd:\BaiduNetdiskDownload\CheatEvolution\CheatEvolution\CheatEvolution.exe'])
time.sleep(2)

print("Starting CheatEvolution_patched.exe under debugger...")
res = kernel32.CreateProcessW(
    r'd:\BaiduNetdiskDownload\CheatEvolution\CheatEvolution\CheatEvolution_patched.exe',
    None, None, None, False,
    DEBUG_PROCESS | DEBUG_ONLY_THIS_PROCESS,
    None, None,
    ctypes.byref(si), ctypes.byref(pi)
)

if not res:
    print("CreateProcess failed")
    ce_proc.kill()
    sys.exit(1)

# we need to find the address of WriteProcessMemory in the child process
# For simplicity, since kernel32 is mapped at the same address in all processes:
wpm_addr = kernel32.GetProcAddress(kernel32.GetModuleHandleW("kernel32.dll"), b"WriteProcessMemory")
print(f"WriteProcessMemory is at {hex(wpm_addr)}")

# Write a breakpoint (0xCC) at WriteProcessMemory
original_byte = ctypes.c_byte()
bytes_read = ctypes.c_size_t(0)
kernel32.ReadProcessMemory(pi.hProcess, wpm_addr, ctypes.byref(original_byte), 1, ctypes.byref(bytes_read))

bp = ctypes.c_byte(0xCC)
kernel32.WriteProcessMemory(pi.hProcess, wpm_addr, ctypes.byref(bp), 1, None)

dbg_event = DEBUG_EVENT()

class CONTEXT64(ctypes.Structure):
    _pack_ = 16
    _fields_ = [
        ("P1Home", ctypes.c_uint64),
        ("P2Home", ctypes.c_uint64),
        ("P3Home", ctypes.c_uint64),
        ("P4Home", ctypes.c_uint64),
        ("P5Home", ctypes.c_uint64),
        ("P6Home", ctypes.c_uint64),
        ("ContextFlags", ctypes.wintypes.DWORD),
        ("MxCsr", ctypes.wintypes.DWORD),
        ("SegCs", ctypes.wintypes.WORD),
        ("SegDs", ctypes.wintypes.WORD),
        ("SegEs", ctypes.wintypes.WORD),
        ("SegFs", ctypes.wintypes.WORD),
        ("SegGs", ctypes.wintypes.WORD),
        ("SegSs", ctypes.wintypes.WORD),
        ("EFlags", ctypes.wintypes.DWORD),
        ("Dr0", ctypes.c_uint64),
        ("Dr1", ctypes.c_uint64),
        ("Dr2", ctypes.c_uint64),
        ("Dr3", ctypes.c_uint64),
        ("Dr6", ctypes.c_uint64),
        ("Dr7", ctypes.c_uint64),
        ("Rax", ctypes.c_uint64),
        ("Rcx", ctypes.c_uint64),
        ("Rdx", ctypes.c_uint64),
        ("Rbx", ctypes.c_uint64),
        ("Rsp", ctypes.c_uint64),
        ("Rbp", ctypes.c_uint64),
        ("Rsi", ctypes.c_uint64),
        ("Rdi", ctypes.c_uint64),
        ("R8", ctypes.c_uint64),
        ("R9", ctypes.c_uint64),
        ("R10", ctypes.c_uint64),
        ("R11", ctypes.c_uint64),
        ("R12", ctypes.c_uint64),
        ("R13", ctypes.c_uint64),
        ("R14", ctypes.c_uint64),
        ("R15", ctypes.c_uint64),
        ("Rip", ctypes.c_uint64),
        # FPU...
    ]

CONTEXT_FULL = 0x10000b

print("Debugging loop started...")
while True:
    if not kernel32.WaitForDebugEvent(ctypes.byref(dbg_event), 1000):
        continue
        
    if dbg_event.dwDebugEventCode == 3: # CREATE_PROCESS_DEBUG_EVENT
        pass
    elif dbg_event.dwDebugEventCode == 1: # EXCEPTION_DEBUG_EVENT
        # We hit our breakpoint
        ctx = CONTEXT64()
        ctx.ContextFlags = CONTEXT_FULL
        hThread = kernel32.OpenThread(0x1F03FF, False, dbg_event.dwThreadId)
        kernel32.GetThreadContext(hThread, ctypes.byref(ctx))
        
        if ctx.Rip - 1 == wpm_addr or ctx.Rip == wpm_addr:
            print(f"WriteProcessMemory Called!")
            print(f"hProcess: {hex(ctx.Rcx)}")
            print(f"lpBaseAddress: {hex(ctx.Rdx)}")
            print(f"lpBuffer: {hex(ctx.R8)}")
            print(f"nSize: {ctx.R9}")
            
            # Read the buffer from the patcher process
            if ctx.R9 > 0:
                buf = ctypes.create_string_buffer(ctx.R9)
                kernel32.ReadProcessMemory(pi.hProcess, ctx.R8, buf, ctx.R9, None)
                print("Bytes written:", buf.raw.hex())
            
            # Restore original byte, step back, and continue
            kernel32.WriteProcessMemory(pi.hProcess, wpm_addr, ctypes.byref(original_byte), 1, None)
            ctx.Rip = wpm_addr
            kernel32.SetThreadContext(hThread, ctypes.byref(ctx))
            
            kernel32.CloseThread(hThread)
            kernel32.ContinueDebugEvent(dbg_event.dwProcessId, dbg_event.dwThreadId, 0x00010002) # DBG_CONTINUE
            
            # We can re-apply breakpoint if we want to catch it again, but we just need one or two.
            # We will exit after catching a few
            # continue
            
    elif dbg_event.dwDebugEventCode == 5: # EXIT_PROCESS_DEBUG_EVENT
        print("Process exited")
        break
        
    kernel32.ContinueDebugEvent(dbg_event.dwProcessId, dbg_event.dwThreadId, 0x80010001) # DBG_EXCEPTION_NOT_HANDLED

ce_proc.kill()
