import cv2
import serial
import time
from ultralytics import YOLO

# Initialize YOLOv8 model
model = YOLO("yolov8n.pt")  # Ensure 'yolov8n.pt' is available

# Initialize Arduino serial communication
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Allow time for Arduino to reset

# Initialize webcam
cap = cv2.VideoCapture(0)

# Define confidence threshold
CONFIDENCE_THRESHOLD = 0.5

try:
    print("Starting detection. Press 'q' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Camera not accessible")
            break

        # Run YOLOv8 inference
        results = model(frame)  # This returns a list of Results objects

        # Process detections
        detected_cat = False

        for r in results:  # Iterate through each Results object
            boxes = r.boxes  # Access the bounding boxes

            for box in boxes:  # Iterate through each box
                conf = box.conf[0]  # Confidence score
                cls = int(box.cls[0])  # Class index

                # Check if it's a cat and confidence is above threshold
                if conf > CONFIDENCE_THRESHOLD and model.names[cls] == "stop sign":
                    detected_cat = True
                    print("Cat detected!")
                    break

        # Send signal to Arduino
        if detected_cat:
            arduino.write(b'1')  # Turn on the LED
        else:
            arduino.write(b'0')  # Turn off the LED

        # Show the frame
        #cv2.imshow("YOLOv8 Detection", frame)
        cv2.imwrite("frame.jpg", frame)

except KeyboardInterrupt:
    print("Detection stopped manually.")
finally:
    cap.release()
    arduino.close()
    #cv2.destroyAllWindows()
    print("Resources released.")
