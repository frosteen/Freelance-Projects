//#include <SoftwareSerial.h>

//SoftwareSerial mySerial(2,3);
#define	READYPIN	9	// pin 9 Ready input


/*  Serial Dot Matrix connections to gizDuino/Arduino
 	gizDuinoPLUS	->	Serial Dot Matrix
 	pin 3			J3-RXD	
 	pin 9			J2-DS
 	GND			J3-GND
 
  	J2- DS is Serial Dot Matrix output telling gizDuino/Arduino it has completed
 		its task and is ready to receive new command (DS LOW=BUSY, DS HIGH=READY).
 
 Note: (This example is for gizduinoPLUS ATMEGA644P with Hardware mySerial)
 If you are using gizDuino UNO, use the SoftwareSerial Library from mySerial to mySerial.
 
COMMANDS:
 Message Animation
       KeyChar HEX
       ESC     1B
       0       00
       1       01
       2       02
       U       55
       D       44
       S       53
       A       41
 Post Message Animations
       s       73
       d       64
       u       75
       f       66
 Message Positioning
       C       43
       L       4C
       R       52
 Test  T       T or 54
 ex. add "\x" before the HEX value of a key character
     for [ESC] =  "\x1B" then add carriage return character "\r" or newline character "\n"
     It shoud be like this: "Serial.print("\x1B\r");"
 
 Codes by e-Gizmo Mechatronix Central
 http://wwww.e-gizmo.com
 October 26, 2017
 */
#include<SoftwareSerial.h>
SoftwareSerial mySerial(2,3);

void  wait_till_ready(void){
  int   i;

  //  Give time for the display unit to activate busy output
  for(i=0;i<1000;i++){
    if(digitalRead(READYPIN)==0) break;
  }

  //wait until ready
  while(digitalRead(READYPIN==0));
}


void setup(){
  mySerial.begin(9600);
  Serial.begin(9600);
  delay(1000);
  // “\x1B” = ESC character
  mySerial.print("\x1B\x1B\r"); 	//[ESC] + [ESC] clear display
}

String str;

void loop(){
  if (Serial.available() > 0) {
    str = Serial.readString();
  }
  else {
    mySerial.print("\x1B\x41");
    mySerial.print(str); //Display your messages here
    mySerial.print("\r"); // [Enter] Send your command
    delay(2000);
    
    //ESC+s = Run the message display until it cleared
    mySerial.print("\x1B\x73\r");
    delay(7000);
  
    mySerial.print("\x1B\x1B\r"); // [ESC] + [ESC]  Clear the display
    delay(100);
  }
}


