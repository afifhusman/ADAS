```shell
#!/bin/bash

# Set variables
SKETCH_FILE=$1  # The first argument to the script is the .ino file
BOARD_FQBN="arduino:avr:mega"  # Board Fully Qualified Name (Change this if needed)

# Check if a sketch file is provided
if [ -z "$SKETCH_FILE" ]; then
    echo "Usage: $0 <sketch_file.ino>"
    exit 1
fi

# Extract filename and directory
SKETCH_NAME=$(basename "$SKETCH_FILE" .ino)
SKETCH_DIR=$(dirname "$SKETCH_FILE")/$SKETCH_NAME

# Ensure the sketch is in a properly named directory
if [ ! -d "$SKETCH_DIR" ]; then
    echo "Creating directory structure for $SKETCH_NAME..."
    mkdir -p "$SKETCH_DIR"
    mv "$SKETCH_FILE" "$SKETCH_DIR/$SKETCH_NAME.ino"
    SKETCH_FILE="$SKETCH_DIR/$SKETCH_NAME.ino"
fi

# Auto-detect the serial port
echo "Detecting Arduino serial port..."
SERIAL_PORT=$(arduino-cli board list | awk '/arduino/{print $1; exit}')
if [ -z "$SERIAL_PORT" ]; then
    echo "No Arduino board detected. Please check the connection."
    exit 1
fi
echo "Arduino detected on port: $SERIAL_PORT"

# Compile the Arduino sketch
echo "Compiling $SKETCH_FILE..."
arduino-cli compile --fqbn $BOARD_FQBN "$SKETCH_DIR"
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Upload the compiled sketch
echo "Uploading $SKETCH_FILE to Arduino on port $SERIAL_PORT..."
arduino-cli upload -p $SERIAL_PORT --fqbn $BOARD_FQBN "$SKETCH_DIR"
if [ $? -eq 0 ]; then
    echo "Upload successful!"
else
    echo "Upload failed!"
    exit 1
fi

```
