import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

# Load pre-trained hand detection model
detector = htm.handDetector()

# Load pre-trained gesture recognition model (replace this with your custom model)
# For demonstration purposes, we'll use a dictionary to map detected landmarks to gestures
gesture_map = {0: "Thumbs Up", 1: "Victory Sign", 2: "Other Gesture"}

# Function to recognize gesture based on detected landmarks
def recognize_gesture(lmList):
    # Example logic: Check the position of specific landmarks to determine the gesture
    if len(lmList) == 21:  # Assuming 21 hand landmarks are detected
        # Check the position of landmarks to recognize gestures
        # For simplicity, let's assume a static gesture where fingers are straight for thumbs up
        if lmList[4][2] < lmList[3][2] and lmList[8][2] < lmList[7][2] and lmList[12][2] < lmList[11][2]:
            return 0  # Thumbs Up
        # For victory sign, we can check if the index and middle fingers are raised while others are down
        elif lmList[8][2] < lmList[7][2] and lmList[12][2] < lmList[11][2]:
            return 1  # Victory Sign
        # Add more conditions to recognize other gestures as needed
    return 2  # Other Gesture by default

# Open the camera
cap = cv2.VideoCapture(0)

# Initialize previous time variable
pTime = 0

# Main loop
while True:
    # Read a frame from the camera
    success, img = cap.read()
    if not success:
        print("Failed to read frame from camera")
        continue

    # Find hands in the frame
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    # Check if any hand landmarks are detected
    if len(lmList) != 0:
        # Recognize gesture based on detected landmarks
        gesture_id = recognize_gesture(lmList)
        gesture = gesture_map.get(gesture_id, "Unknown")
        print("Detected Gesture:", gesture)

        # Display recognized gesture on the frame
        cv2.putText(img, "Gesture: " + gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display FPS on the frame
    cv2.putText(img, "FPS: " + str(int(1 / (time.time() - pTime))), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    pTime = time.time()  # Update previous time

    # Display the frame
    cv2.imshow("Camera", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()



