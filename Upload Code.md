```c
#!/bin/bash

# Set variables
SKETCH_FILE=$1  # The first argument to the script is the .ino file
BOARD_FQBN="arduino:avr:uno"  # Change to your board's FQBN
SERIAL_PORT="/dev/ttyACM0"    # Adjust to your Arduino's serial port

# Check if a sketch file is provided
if [ -z "$SKETCH_FILE" ]; then
    echo "Usage: $0 <sketch_file.ino>"
    exit 1
fi

# Compile the Arduino sketch
echo "Compiling $SKETCH_FILE..."
arduino-cli compile --fqbn $BOARD_FQBN $SKETCH_FILE
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Upload the compiled sketch
echo "Uploading $SKETCH_FILE to Arduino..."
arduino-cli upload -p $SERIAL_PORT --fqbn $BOARD_FQBN $SKETCH_FILE
if [ $? -eq 0 ]; then
    echo "Upload successful!"
else
    echo "Upload failed!"
    exit 1
fi
```