#This code doesn't use mediapipe

import cv2
import numpy as np

# Function to recognize hand gesture
def recognize_gesture(contour, threshold):
    hull = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull)
    if defects is not None:
        count_defects = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            if d > threshold:  # Adjust this threshold based on your environment
                count_defects += 1
                cv2.circle(frame, far, 3, [255, 0, 0], -1)
            cv2.line(frame, start, end, [0, 255, 0], 2)
        
        # Based on the number of defects, recognize the gesture
        if count_defects == 0:
            return "👍"  # Thumbs up
        elif count_defects == 1:
            return "✌️"  # Victory
        elif count_defects == 2:
            return "☝️"  # Pointing up
        elif count_defects == 3:
            return "✊"   # Closed fist
        elif count_defects == 4:
            return "👋"   # Open palm
        elif count_defects == 5:
            return "🤟"   # I love you
        elif count_defects > 5:
            return "👎"   # Thumbs down
    
    return None

# Capture video from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Thresholding
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Ensure contours were found
    if contours:
        # Find the contour with maximum area
        max_contour = max(contours, key=cv2.contourArea)
        # Recognize gestures based on contour and threshold
        gesture_text = recognize_gesture(max_contour, 10000)
        #if gesture_text:
            # Display gesture
           # font = cv2.FONT_HERSHEY_SIMPLEX
          #  cv2.putText(frame, gesture_text, (50, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
    
    # Display frame
    cv2.imshow('Hand Gesture Recognition', frame)
    
    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
