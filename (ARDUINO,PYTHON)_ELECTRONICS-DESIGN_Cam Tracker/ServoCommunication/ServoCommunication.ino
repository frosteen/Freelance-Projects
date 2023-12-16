#include<Servo.h>

Servo servoVer; //Vertical Servo
Servo servoHor; //Horizontal Servo

int x;
int y;

//Initial stop values
double initialX = 90;
double distanceX = 0.1; //distance of min and max to initialX
double initialY = 90;
double distanceY = 0.1; //distance of min and max to initialY
double speeder = 2;

int prevX; //previous x values
int prevY; //previous y values

void setup()
{
  Serial.begin(9600); //begin at 9600 baud rate
  servoVer.attach(5); //attach Vertical Servo to Pin 5
  servoHor.attach(6); //attach Horizontal Servo to Pin 6

  //start initial values of motor
  servoHor.write(initialX);
  servoVer.write(initialY);
}

//position function
double servoX = initialX;
double servoY = initialY;
void Pos()
{
  if (prevX != x || prevY != y) //if position is not always
  {
    if (servoX-speeder > -10 && servoX+speeder < 190) {
      if (x < 150) {
        servoX = servoX + distanceX + speeder;
        servoHor.write(servoX);
      }
      else if (x < 250) {
        servoX = servoX + distanceX;
        servoHor.write(servoX);
      }
      if (x > 350) {
        servoX = servoX - distanceX - speeder;
        servoHor.write(servoX);
      }
      else if (x > 250) {
        servoX = servoX - distanceX;
        servoHor.write(servoX);
      }
    }
    else {
      servoX = 90;
    }

    
    if (servoY - speeder > 70 && servoY+speeder < 180) {
      if (y < 150) {
        servoY = servoY + distanceY + speeder;
        servoVer.write(servoY);
      }
      else if (y < 250) {
        servoY = servoY + distanceY;
        servoVer.write(servoY);
      }
      if (y > 350) {
        servoY = servoY - distanceY - speeder;
        servoVer.write(servoY);
      }
      else if (y > 250) {
        servoY = servoY - distanceY;
        servoVer.write(servoY);
      }
      Serial.println(servoY);
    }
    else {
      servoY = 90;
    }
    prevX = x;
    prevY = y;
  }
}

void loop()
{
  if (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == 'X') //if character X is found
    {
      x = Serial.parseInt(); //get the next integer value
      if (Serial.read() == 'Y') //if character Y is found
      {
        y = Serial.parseInt(); //get the next integer value
        Pos(); //response to change in position
      }
      Serial.println(String(x) + "-" + String(y));
    }
    else if (c == 'A') { //if character A is found
      servoVer.attach(5); //Attach Vertical Servo to Pin 5
      servoHor.attach(6); //Attach Horizontal Servo to Pin 6

      //return to original position
      servoHor.write(initialX);
      servoVer.write(initialY);
      Serial.println("A");
    }
    else if (c == 'D') { //if character D is found
      //turn off the servo
      servoVer.detach();
      servoHor.detach();
      Serial.println("D");
    }
  }
}


