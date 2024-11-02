import pymem
import pyuac
from pyuac import main_requires_admin

def read_memory(pm, address, size):
    try:
        raw_bytes = pm.read_bytes(address, size)
        return raw_bytes
    except pymem.exception.MemoryReadError as e:
        print(f"Could not read memory at address {hex(address)}: {e}")
        return None

@main_requires_admin
def main():
    # Open Dolphin process
    try:
        pm = pymem.Pymem('Dolphin.exe')
        print("Successfully attached to Dolphin process.")
    except pymem.exception.ProcessNotFound:
        print("Dolphin process not found. Please make sure Dolphin is running.")
        return

    # Example static memory address in Dolphin's process space (replace with actual known address)
    test_address = 0x8154B8B0  # This is an example; replace with a known valid address
    read_size = 4  # Number of bytes to read

    while True:
        data = read_memory(pm, test_address, read_size)
        if data is not None:
            print(f"Data at address {hex(test_address)}: {data}")
        else:
            print("Failed to read data. Check if the address is correct and the game is running.")
        
        break  # Exit after one read for simplicity

if __name__ == "__main__":
    main()

