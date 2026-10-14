import cv2
import numpy as np
import mediapipe as mp

# 1. Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Width
cap.set(4, 720)  # Height

# 2. MediaPipe Initialization
mpHands = mp.solutions.hands
# Increased confidence thresholds slightly to prevent jitter while drawing
hands = mpHands.Hands(min_detection_confidence=0.85, min_tracking_confidence=0.85)
mpDraw = mp.solutions.drawing_utils

# 3. Drawing Variables
brushThickness = 7
eraserThickness = 50
drawColor = (0, 0, 255) # Default to Red (BGR format)
xp, yp = 0, 0 # Previous x and y coordinates for smooth lines

# Create a blank black canvas to draw on
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally so it acts like a mirror
    img = cv2.flip(img, 1)
    
    # Optional: Boost brightness if you are still in a low-light room
    img = cv2.convertScaleAbs(img, alpha=1.2, beta=30)

    # 4. Draw the Color Palette UI at the top of the screen
    # Red, Green, Blue, and Eraser rectangles
    cv2.rectangle(img, (50, 20), (250, 100), (0, 0, 255), cv2.FILLED) # Red
    cv2.rectangle(img, (350, 20), (550, 100), (0, 255, 0), cv2.FILLED) # Green
    cv2.rectangle(img, (650, 20), (850, 100), (255, 0, 0), cv2.FILLED) # Blue
    cv2.rectangle(img, (950, 20), (1150, 100), (255, 255, 255), cv2.FILLED) # Eraser
    cv2.putText(img, "ERASER", (1000, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)

    # 5. Process Hand Tracking
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if len(lmList) != 0:
        # Get coordinates for Index (8) and Middle (12) fingertips
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]

        # Check which fingers are up
        # If the tip (8/12) is higher than the PIP joint (6/10), the finger is up
        fingers = []
        fingers.append(1 if lmList[8][2] < lmList[6][2] else 0)  # Index
        fingers.append(1 if lmList[12][2] < lmList[10][2] else 0) # Middle

        # --- SELECTION MODE (Index and Middle fingers are UP) ---
        if fingers[0] == 1 and fingers[1] == 1:
            xp, yp = 0, 0 # Reset previous coordinates to prevent connecting lines
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            
            # Check if selecting a color in the header
            if y1 < 100:
                if 50 < x1 < 250:
                    drawColor = (0, 0, 255) # Red
                elif 350 < x1 < 550:
                    drawColor = (0, 255, 0) # Green
                elif 650 < x1 < 850:
                    drawColor = (255, 0, 0) # Blue
                elif 950 < x1 < 1150:
                    drawColor = (0, 0, 0) # Eraser (Black)

        # --- DRAWING MODE (Only Index finger is UP) ---
        if fingers[0] == 1 and fingers[1] == 0:
            cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
            
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0): # If Eraser
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else: # If Drawing
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1 # Update previous coordinates

    # 6. Merge the Canvas and the Camera Feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    
    # Overlay the drawings seamlessly onto the video
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    cv2.imshow("Air Canvas", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()