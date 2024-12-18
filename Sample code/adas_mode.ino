// Pin definitions
#define ENA 5  // PWM control for Motor A
#define IN1 3  // Direction control for Motor A
#define IN2 4

#define ENB 6 // PWM control for Motor B
#define IN3 11 // Direction control for Motor B
#define IN4 12

void setup() {
  // Set control pins as outputs
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Start serial communication
  Serial.begin(9600);
  Serial.println("Waiting for commands...");
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming byte

    if (command == '0') {
      // Move both motors forward
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      analogWrite(ENA, 70); // Speed control for Motor A

      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      analogWrite(ENB, 70); // Speed control for Motor B

      Serial.println("Motors moving forward");
    } else if (command == '1') {
      // Stop both motors
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      analogWrite(ENA, 0); // Stop Motor A

      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      analogWrite(ENB, 0); // Stop Motor B

      Serial.println("Motors stopped");
    } else {
      // Invalid command received
      Serial.println("Invalid command");
    }
  }
}