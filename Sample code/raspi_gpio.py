import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 17  # Change this to the GPIO pin you're using

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setup(LED_PIN, GPIO.OUT)  # Set the pin as an output

try:
    print("Turning LED ON...")
    GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
    time.sleep(5)  # Keep LED on for 5 seconds
    
    print("Turning LED OFF...")
    GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
