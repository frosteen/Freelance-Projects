#include <Servo.h>
Servo servo;
const int IR_PIN = 5;
const int RELAY_PIN = 6;
int value;
void setup()
{
  servo.attach(9);            // The servo motor is connected to D9
  pinMode(IR_PIN, INPUT);     // Configure the pin of the IR_PIN as INPUT
  pinMode(RELAY_PIN, OUTPUT); // Configure the pin of the relay module as OUTPUT
  Serial.begin(9600);         // Set baud rate as 9600
}
void loop()
{
  value = digitalRead(IR_PIN); // Read the digital signal sent by the IR_PIN and store it in the 'value' variable
  // Serial.print("Status of IR_PIN: ");
  // Serial.println(value);
  if (value == LOW)
  { // If you place your hands in front of the IR_PIN after washing your hands
    servo.write(90);
    delay(10000); // The door will be opened for 10 seconds
    servo.write(0);
  }
}