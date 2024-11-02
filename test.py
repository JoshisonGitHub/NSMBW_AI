import pymem
import time

# Addresses for Mario's X and Y positions (replace these with your values)
MARIO_X_ADDR = 0x8154B8B0  # Replace with the actual address for Mario's X position
MARIO_Y_ADDR = 0x8154B8B4  # Replace with the actual address for Mario's Y position

# Dolphin process name (ensure it's running)
PROCESS_NAME = "Dolphin.exe"

def read_position():
    try:
        # Open Dolphin process
        dolphin = pymem.Pymem(PROCESS_NAME)
        
        # Read Mario's position values periodically
        print("Reading Mario's X and Y positions. Press Ctrl+C to stop.")
        while True:
            mario_x = dolphin.read_float(MARIO_X_ADDR)
            mario_y = dolphin.read_float(MARIO_Y_ADDR)
            
            print(f"Mario's Position -> X: {mario_x}, Y: {mario_y}")
            
            # Wait before reading again
            time.sleep(0.5)  # Adjust as needed (e.g., every half second)
    except pymem.exception.ProcessNotFound:
        print("Dolphin emulator process not found. Ensure Dolphin is running.")
    except pymem.exception.MemoryReadError:
        print("Could not read memory. Check if the addresses are correct or try running the script as administrator.")
    except KeyboardInterrupt:
        print("Stopped reading Mario's position.")

# Run the position reading function
read_position()
