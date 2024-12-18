import cv2
import numpy as np
from ultralytics import YOLO
import serial
import time
from typing import Tuple, Optional
import threading
from queue import Queue
import torch

# Constants
CONFIDENCE_THRESHOLD = 0.5
STOP_SIGN_CLASS = 11  # COCO dataset class index for stop sign
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
FRAME_WIDTH = 416  # Reduced from 640 for better performance
FRAME_HEIGHT = 416  # Square input for optimal YOLO performance
QUEUE_SIZE = 1
DETECTION_INTERVAL = 0.1  # 100ms between detections

class StopSignDetector:
    def __init__(self) -> None:
        # Enable hardware acceleration if available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if self.device == 'cpu':
            torch.set_num_threads(4)  # Optimize CPU threading for Pi 4
        
        # Initialize YOLOv8 model with optimization
        self.model = YOLO('yolov8n.pt')
        self.model.to(self.device)
        
        # Initialize camera with optimal settings
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, 15)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        
        # Initialize serial connection
        try:
            self.serial_conn = serial.Serial(
                port=SERIAL_PORT,
                baudrate=BAUD_RATE,
                timeout=1,
                write_timeout=0.1
            )
            time.sleep(2)  # Allow Arduino to reset
        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
            raise

        # Initialize threading components
        self.frame_queue = Queue(maxsize=QUEUE_SIZE)
        self.result_queue = Queue(maxsize=QUEUE_SIZE)
        self.running = True

    def capture_frames(self) -> None:
        """Thread function for continuous frame capture."""
        while self.running:
            frame = self.read_frame()
            if frame is not None:
                if self.frame_queue.full():
                    self.frame_queue.get()  # Remove old frame
                self.frame_queue.put(frame)
            time.sleep(0.01)  # Small delay to prevent CPU overload

    def process_frames(self) -> None:
        """Thread function for frame processing."""
        last_detection_time = 0
        while self.running:
            current_time = time.time()
            if current_time - last_detection_time < DETECTION_INTERVAL:
                time.sleep(0.01)
                continue

            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                stop_detected = self.detect_stop_sign(frame)
                if self.result_queue.full():
                    self.result_queue.get()
                self.result_queue.put(stop_detected)
                last_detection_time = current_time

    def read_frame(self) -> Optional[np.ndarray]:
        """Efficiently read and preprocess a frame."""
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        # Optimize frame preprocessing
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT), 
                         interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert once, early

    @torch.no_grad()  # Disable gradient computation for inference
    def detect_stop_sign(self, frame: np.ndarray) -> bool:
        """Optimized stop sign detection."""
        # Convert to tensor and normalize in single operation
        img = torch.from_numpy(frame).to(self.device).float()
        img = img.permute(2, 0, 1) / 255.0
        img = img.unsqueeze(0)  # Add batch dimension
        
        # Run inference with optimization flags
        results = self.model(img, verbose=False)[0]
        
        # Efficient detection check
        for det in results.boxes.data:
            if int(det[5]) == STOP_SIGN_CLASS and float(det[4]) > CONFIDENCE_THRESHOLD:
                return True
        return False

    def send_signal(self, stop_detected: bool) -> None:
        """Send detection result to Arduino with timeout."""
        signal = b'1' if stop_detected else b'0'
        try:
            self.serial_conn.write(signal)
        except serial.SerialException as e:
            print(f"Serial write error: {e}")

    def cleanup(self) -> None:
        """Release resources."""
        self.running = False
        self.cap.release()
        self.serial_conn.close()
        cv2.destroyAllWindows()

    def run(self) -> None:
        """Main detection loop with threaded processing."""
        # Start threads
        capture_thread = threading.Thread(target=self.capture_frames)
        process_thread = threading.Thread(target=self.process_frames)
        
        capture_thread.start()
        process_thread.start()

        try:
            while True:
                if not self.result_queue.empty():
                    stop_detected = self.result_queue.get()
                    self.send_signal(stop_detected)
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("\nStopping detection...")
        finally:
            self.cleanup()
            capture_thread.join()
            process_thread.join()

if __name__ == "__main__":
    try:
        detector = StopSignDetector()
        detector.run()
    except Exception as e:
        print(f"Error: {e}")