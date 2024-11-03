import cv2
import numpy as np
import keyboard
import time

STRUM = "up arrow"

vid_device_number = 1

# note colors
color_definitions = {
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "BLUE": (0, 0, 255),
    "ORANGE": (255, 165, 0),
    "OPEN": (128, 0, 128)
}

# RGB to HSV
def rgb_to_hsv(color):
    bgr_color = np.uint8([[color]]) 
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    return hsv_color[0][0]

# note color range
hsv_colors = {
    "GREEN": (np.array([60, 200, 200]), np.array([65, 255, 255])),      
    "RED": [
        (np.array([0, 150, 150]), np.array([10, 255, 255])),            
        (np.array([170, 150, 150]), np.array([180, 255, 255]))          
    ],
    "YELLOW": (np.array([32, 200, 200]), np.array([33, 255, 255])),   
    "BLUE": (np.array([95, 150, 150]), np.array([135, 255, 255])),    
    "ORANGE": (np.array([15, 200, 200]), np.array([25, 255, 255])),    
    "OPEN": (np.array([135, 200, 200]), np.array([168, 255, 255]))   
}

# color to input mapping
color_to_letter = {
    "GREEN": "a",
    "RED": "s",
    "YELLOW": "d",
    "BLUE": "f",
    "ORANGE": "j",
    "OPEN": "up"
}

cap = cv2.VideoCapture(1)

run_detection = False

while True:

    start = time.time()

    # k = kill key
    if keyboard.is_pressed('k'):
        print("Exiting program.")
        break
    
    # l = start key
    if keyboard.is_pressed('l'):
        print("Starting detection.")
        run_detection = True

    if run_detection:

        ret, frame = cap.read()
        if not ret:
            break
        
        # grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # threshold for what is considered black
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if cv2.contourArea(c) > 100]
        
        if contours:
            # get bounding box
            x, y, w, h = cv2.boundingRect(np.vstack(contours))
            cropped_frame = frame[y:y+h, x:x+w]
            hsv_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
            
            # colors found
            detected_colors = []

            for color_name, hsv_range in hsv_colors.items():
                if color_name == "RED":
                    # special case for red with two ranges
                    mask1 = cv2.inRange(hsv_frame, hsv_range[0][0], hsv_range[0][1])
                    mask2 = cv2.inRange(hsv_frame, hsv_range[1][0], hsv_range[1][1])
                    mask = cv2.bitwise_or(mask1, mask2)
                else:
                    # single range for other colors
                    lower, upper = hsv_range
                    mask = cv2.inRange(hsv_frame, lower, upper)
                
                # check if any pixels match this color
                if cv2.countNonZero(mask) > 0:
                    detected_colors.append(color_name)
            
            # hit keys corresponding to colors
            if detected_colors:
                converted_letters = [color_to_letter[color] for color in detected_colors if color in color_to_letter]
                print("Detected colors:", converted_letters)
                for key in converted_letters:
                        if key != "up":
                            keyboard.press(key)
                keyboard.press(STRUM)
                for key in converted_letters:
                    keyboard.release(key)
                keyboard.release(STRUM)
            cv2.imshow('Cropped Frame', cropped_frame)
        else:
            print("No non-black regions found.")
            cv2.imshow('Cropped Frame', frame)

    end = time.time()  

cap.release()
cv2.destroyAllWindows()







