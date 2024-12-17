1. Install Arduino CLI
```Shell
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
```

2. Move the CLI binary to the system path
```Shell
sudo mv bin/arduino-cli /usr/local/bin/
```

3. Initialize Arduino CLI
```Shell
arduino-cli config init
```

4. Update the core index and install board definitions
```Shell
arduino-cli core update-index
arduino-cli core install arduino:avr
```

4. Connect the arduino to raspberry pi. Then, verify the board is connected
```Shell
arduino-cli board list
```

Note the serial port of the Arduino (e.g., /dev/ttyACM0)

