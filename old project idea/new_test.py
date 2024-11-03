import pymem
import re
from pyuac import main_requires_admin

PROCESS_NAME = "Dolphin.exe"


@main_requires_admin
def main():
    with open('locations.md', 'r') as file:
        # Iterate through each line in the file
        next(file)
        for line in file:
            # Search for a hex pattern (e.g., 8-character hex value)
            match = re.search(r'\b[0-9A-Fa-f]+\b', line)
            if match:
                hex_value = match.group(0)
            KNOWN_ADDRESS = int('0x' + hex_value, 16)
        
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

if __name__ == "__main__":
    main()
