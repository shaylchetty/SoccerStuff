import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)

prevY = 0
juggle_in_progress = False  # Flag to track if a juggle is currently being counted
juggles = 0

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds of the average yellow color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    
    # Create a mask using the color range
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If contours are found, filter and draw the largest one
    if len(contours) > 0:
        for contour in contours:
            area = cv2.contourArea(contour)
            if 15000 < area:  # Set your desired size range here
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                
                # Draw the circle around the ball
                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 4)
                    cv2.circle(frame, (int(x), int(y)), int(radius//10), (0, 0, 255), 3)
                    if (prevY) == 0:
                        prevY = int(y)
                        continue
                    if y > prevY + 50 and not juggle_in_progress:
                        juggle_in_progress = True
                        juggles += 1
                        print(juggles)
                    elif y <= prevY:
                        juggle_in_progress = False
                    prevY = int(y)
                    
                break

    # Display the number of juggles at the top center of the frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f'Juggles: {juggles}'
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = text_size[1] + 50
    cv2.putText(frame, text, (text_x, text_y), font, 3, (0, 255, 0), 3, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Juggle Counting', frame)
    
    # Exit the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
