import pymem
import pymem.process
import struct
import time

def read_float(pm, address):
    raw_bytes = pm.read_bytes(address, 4)
    return struct.unpack('f', raw_bytes)[0]

def read_int(pm, address):
    raw_bytes = pm.read_bytes(address, 4)
    return struct.unpack('i', raw_bytes)[0]

def read_byte(pm, address):
    raw_bytes = pm.read_bytes(address, 1)
    return struct.unpack('B', raw_bytes)[0]

def get_player_coordinates(pm, x_address, y_address):
    try:
        x = read_float(pm, x_address)
        y = read_float(pm, y_address)
        return x, y
    except pymem.exception.MemoryReadError as e:
        print(f"Could not read coordinates at addresses {hex(x_address)} and {hex(y_address)}: {e}")
        return None, None

def check_player_life_status(pm, life_status_address):
    try:
        status = read_byte(pm, life_status_address)  # Assuming death status is stored as a byte
        return status == 0  # Assuming 0 means dead and 1 means alive
    except pymem.exception.MemoryReadError as e:
        print(f"Could not read life status at address {hex(life_status_address)}: {e}")
        return False

def main():
    # Open Dolphin process
    pm = pymem.Pymem('Dolphin.exe')
    module = pymem.process.module_from_name(pm.process_handle, 'Dolphin.exe').lpBaseOfDll

    # Use the verified addresses
    x_address = 0x8120ADF4  # Replace with the correct value
    y_address = 0x815E38E4  # Replace with the correct value
    life_status_address = 0x80429CA3  # Replace with the correct value

    while True:
        x, y = get_player_coordinates(pm, x_address, y_address)
        player_dead = check_player_life_status(pm, life_status_address)
        
        if x is not None and y is not None:
            if player_dead:
                print("Player has died.")
                # Check if coordinates have reset or remained the same
                if x == 0 and y == 0:
                    print("Player coordinates reset to (0, 0) upon death.")
                else:
                    print(f"Player coordinates at death: X={x}, Y={y}")
            else:
                print(f"Player coordinates: X={x}, Y={y}")
        
        time.sleep(0.1)  # Adjust the sleep interval as needed

if __name__ == "__main__":
    main()


