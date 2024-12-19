1. Install Arduino CLI
```Shell
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
```

2. Move the CLI binary to the system path
```
sudo mv bin/arduino-cli /usr/local/bin/
```

3. Initialize Arduino CLI
```
arduino-cli config init
```

4. Update the core index and install board definitions
```
arduino-cli core update-index && arduino-cli core install arduino:avr
```

5. Connect the arduino to raspberry pi. Then, verify the board is connected
```
arduino-cli board list
```

```
wget https://raw.githubusercontent.com/afifhusman/ADAS/refs/heads/main/upload_code.sh -O upload_code && chmod +x upload_code && sudo mv upload_code /usr/local/bin/upload_code
```
Note the serial port of the Arduino (e.g., /dev/ttyACM0)

