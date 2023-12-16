/*
  # Face tracking using arduino - Code #
  # Code by Harsh Dethe
  # 09 Sep 2018.
*/

#include<Servo.h>

Servo servoVer; //Vertical Servo
Servo servoHor; //Horizontal Servo

int x;
int y;

//Initial stop values
int initialX = 86;
int distanceX = 7; //distance of min and max to initialX
int initialY = 80;
int distanceY = 10; //distance of min and max to initialY

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
void Pos()
{
  if(prevX != x || prevY != y) //if position is not always
  {
    //map the 0-250 values to the motor values
    int servoX = map(x, 0, 500, initialX-distanceX, initialX+distanceX+5);
    int servoY = map(y, 0, 500, initialY+distanceY, initialY-distanceY);
    
    servoHor.write(servoX);
    servoVer.write(servoY);

    prevX = x;
    prevY = y;
  }
}

void loop()
{
  if(Serial.available() > 0)
  {
    if(Serial.read() == 'X') //if character X is found
    {
      x = Serial.parseInt(); //get the next integer value
      if(Serial.read() == 'Y') //if character Y is found
      {
        y = Serial.parseInt(); //get the next integer value
       Pos(); //response to change in position
      }
    }
    else if(Serial.read() == 'A') { //if character A is found
      servoVer.attach(5); //Attach Vertical Servo to Pin 5
      servoHor.attach(6); //Attach Horizontal Servo to Pin 6

      //return to original position
      servoHor.write(initialX);
      servoVer.write(initialY);
    }
    else if(Serial.read() == 'D') { //if character D is found
      //turn off the servo
      servoVer.detach();
      servoHor.detach();
    }

    //if character is different then just continue looping
    while(Serial.available() > 0)
    {
      Serial.read();
    }
  }
}
  

