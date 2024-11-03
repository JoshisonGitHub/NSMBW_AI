import cv2
import numpy as np
import keyboard
import time
from input_values import *

# Define the colors in RGB format (for easier reading)
color_definitions = {
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "BLUE": (0, 0, 255),
    "ORANGE": (255, 165, 0),
    "OPEN": (128, 0, 128)  # Purple in RGB
}

# Convert RGB colors to HSV
def rgb_to_hsv(color):
    bgr_color = np.uint8([[color]])  # Convert RGB to BGR for OpenCV
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    return hsv_color[0][0]

# Define specific HSV ranges for each color
hsv_colors = {
    "GREEN": (np.array([60, 200, 200]), np.array([65, 255, 255])),      # Narrowed Green hue range
    "RED": [
        (np.array([0, 150, 150]), np.array([10, 255, 255])),            # Expanded Red lower range
        (np.array([170, 150, 150]), np.array([180, 255, 255]))          # Expanded Red upper range for wrap-around
    ],
    "YELLOW": (np.array([32, 200, 200]), np.array([33, 255, 255])),     # Narrowed Yellow hue range
    "BLUE": (np.array([95, 150, 150]), np.array([135, 255, 255])),      # Expanded Blue hue range
    "ORANGE": (np.array([15, 200, 200]), np.array([25, 255, 255])),     # Reduced Orange hue range
    "OPEN": (np.array([135, 200, 200]), np.array([168, 255, 255]))      # Narrowed Purple hue range
}





# Define color-to-key mapping
color_to_letter = {
    "GREEN": "a",
    "RED": "s",
    "YELLOW": "d",
    "BLUE": "f",
    "ORANGE": "j",
    "OPEN": "up"
}

# Initialize the video capture (change 1 to 0 if necessary)
cap = cv2.VideoCapture(1)

# Flag to control running state
run_detection = False

while True:
    start = time.time()
    # Check if 'K' is pressed to exit
    if keyboard.is_pressed('k'):
        print("Exiting program.")
        break
    
    # Check if 'L' is pressed to start detection
    if keyboard.is_pressed('l'):
        print("Starting detection.")
        run_detection = True  # Set flag to run detection

    # If detection is active, process the frame
    if run_detection:
        # Capture a frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply a threshold to get binary image (non-black pixels are white, black is black)
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter out small contours (optional)
        contours = [c for c in contours if cv2.contourArea(c) > 100]
        
        if contours:
            # Combine all contours to get the bounding box around all non-black areas
            x, y, w, h = cv2.boundingRect(np.vstack(contours))
            
            # Crop the frame to this bounding box
            cropped_frame = frame[y:y+h, x:x+w]
            
            # Convert cropped frame to HSV
            hsv_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
            
            # Check for each color
            detected_colors = []

            for color_name, hsv_range in hsv_colors.items():
                if color_name == "RED":
                    # Special case for red with two ranges
                    mask1 = cv2.inRange(hsv_frame, hsv_range[0][0], hsv_range[0][1])
                    mask2 = cv2.inRange(hsv_frame, hsv_range[1][0], hsv_range[1][1])
                    mask = cv2.bitwise_or(mask1, mask2)
                else:
                    # Single range for other colors
                    lower, upper = hsv_range
                    mask = cv2.inRange(hsv_frame, lower, upper)
                
                # Check if any pixels match this color
                if cv2.countNonZero(mask) > 0:
                    detected_colors.append(color_name)
            
            # Display detected colors and trigger corresponding keys
            if detected_colors:
                converted_letters = [color_to_letter[color] for color in detected_colors if color in color_to_letter]
                print("Detected colors:", converted_letters)
                # Use keyboard.send to press and release each key
                for key in converted_letters:
                        if key != "up":
                            keyboard.press(key)
                keyboard.press(STRUM)
                for key in converted_letters:
                    keyboard.release(key)
                keyboard.release(STRUM)
            # Display the cropped frame
            cv2.imshow('Cropped Frame', cropped_frame)
        else:
            print("No non-black regions found.")
            cv2.imshow('Cropped Frame', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    end = time.time()  
    #time.sleep(10 * (end - start))



# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()







