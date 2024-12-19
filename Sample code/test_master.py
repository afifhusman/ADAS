import serial

# Set up the serial connection
arduino_port = "/dev/ttyACM0"  # Replace with your Arduino's serial port
baud_rate = 9600       # Match this to your Arduino's baud rate

try:
    # Open the serial port
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")

    while True:
        # Wait for user input
        user_input = input("Enter a message to send to Arduino (or 'exit' to quit): ")
        
        # Exit the loop if the user types 'exit'
        if user_input.lower() == 'exit':
            print("Exiting...")
            break
        
        # Send the user input to Arduino
        ser.write(user_input.encode())  # Encode the string to bytes
        print(f"Sent: {user_input}")

        # Optionally, read response from Arduino
        arduino_response = ser.readline().decode().strip()  # Read and decode the response
        if arduino_response:
            print(f"Arduino replied: {arduino_response}")

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
