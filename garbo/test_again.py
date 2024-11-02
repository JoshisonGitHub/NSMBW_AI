import ctypes
from ctypes import wintypes
import re

PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

kernel32 = ctypes.windll.kernel32
pid = 3172  # Replace with the actual Dolphin PID



'''
import psutil

target_process_name = "dolphin"  # Ensure this matches the actual Dolphin executable name
pid = None

for proc in psutil.process_iter(['pid', 'name']):
    if target_process_name.lower() in proc.info['name'].lower():
        pid = proc.info['pid']
        print(f"Found Dolphin PID: {pid}")
        break

if pid is None:
    print("Dolphin process not found.")
else:
    # Use this PID in your main code
    print(f"Dolphin is running with PID: {pid}")
'''

process_handle = kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)

if not process_handle:
    print("Could not get process handle.")
else:
    with open('locations.md', 'r') as file:
        # Iterate through each line in the file
        next(file)
        for line in file:
            # Search for a hex pattern (e.g., 8-character hex value)
            match = re.search(r'\b[0-9A-Fa-f]+\b', line)
            if match:
                hex_value = match.group(0)
            address = int('0x' + hex_value, 16)
            buffer = ctypes.c_int()
            bytes_read = wintypes.SIZE()

            success = kernel32.ReadProcessMemory(process_handle, address, ctypes.byref(buffer), ctypes.sizeof(buffer), ctypes.byref(bytes_read))
            if success:
                print(f"Memory value at {hex(address)}: {buffer.value}")
            else:
                print("Failed to read memory.")

    kernel32.CloseHandle(process_handle)


