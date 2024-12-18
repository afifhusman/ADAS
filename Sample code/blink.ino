void setup() {
  pinMode(13, OUTPUT); // Set pin 13 as an OUTPUT
}

void loop() {
  digitalWrite(13, HIGH); // Turn the LED ON
  delay(1000);            // Wait for 1 second (1000 milliseconds)
  digitalWrite(13, LOW);  // Turn the LED OFF
  delay(1000);            // Wait for 1 second
}
