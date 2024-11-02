import pymem

PROCESS_NAME = "Dolphin.exe"
KNOWN_ADDRESS = 0x811FDF88 # Replace with a known address
KNOWN_ADDRESS = 0x8000063

try:
    # Connect to Dolphin
    dolphin = pymem.Pymem(PROCESS_NAME)
    print("Dolphin emulator process found and accessible!")

    # Attempt to read a known address
    test_value = dolphin.read_float(KNOWN_ADDRESS)
    print(f"Read value at KNOWN_ADDRESS: {test_value}")
except pymem.exception.ProcessNotFound:
    print("Dolphin emulator process not found. Make sure Dolphin is running.")
except pymem.exception.MemoryReadError:
    print("Could not read memory at the specified address. Check if the address is correct or if permissions are needed.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
