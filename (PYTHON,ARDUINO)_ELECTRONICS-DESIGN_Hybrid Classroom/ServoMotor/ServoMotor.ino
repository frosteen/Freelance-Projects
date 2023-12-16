#include <Servo.h>

Servo myservo;
int pos = 90;
int max_pos = 180;
int min_pos = 0;
char key;

void setup()
{
  Serial.begin(9600);
  myservo.attach(9);
}

void loop()
{
  if (Serial.available() > 0) {
    key = Serial.read();
    if ((key == 'B' || key == 'b') && pos < max_pos) {
      pos = pos + 10;
    } else pos = pos;
    if ((key == 'A' || key == 'a') && pos > min_pos) {
      pos = pos - 10;
    } else pos = pos;
  }
  myservo.write(pos);
  //  Serial.println(pos);
}
