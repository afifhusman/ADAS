const int ledPin = 13;  // Built-in LED pin
char receivedData;

void setup() {
  pinMode(ledPin, OUTPUT);  // Set built-in LED pin as OUTPUT
  Serial.begin(9600);       // Start serial communication
}

void loop() {
  if (Serial.available() > 0) {
    receivedData = Serial.read();  // Read incoming data

    if (receivedData == '1') {
      digitalWrite(ledPin, HIGH);  // Turn ON the built-in LED
    } 
    else if (receivedData == '0') {
      digitalWrite(ledPin, LOW);   // Turn OFF the built-in LED
    }
  }
}
