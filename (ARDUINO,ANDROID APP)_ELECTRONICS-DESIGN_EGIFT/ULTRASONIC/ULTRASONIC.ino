
/******************************************************
 * Written by : Usman Ali Butt                        *           
 * Dated      : 1 August 2018                         *
 * Property off:  www.microcontroller-project.com     *
 *****************************************************/

const int trigP = D5;  //D4 Or GPIO-2 of nodemcu
const int echoP = D6;  //D3 Or GPIO-0 of nodemcu

long duration;
int distance;

void setup() {
pinMode(trigP, OUTPUT);  // Sets the trigPin as an Output
pinMode(echoP, INPUT);   // Sets the echoPin as an Input
Serial.begin(9600);      // Open serial channel at 9600 baud rate
}

void loop() {

digitalWrite(trigP, LOW);   // Makes trigPin low
delayMicroseconds(2);       // 2 micro second delay 

digitalWrite(trigP, HIGH);  // tigPin high
delayMicroseconds(10);      // trigPin high for 10 micro seconds
digitalWrite(trigP, LOW);   // trigPin low

duration = pulseIn(echoP, HIGH);   //Read echo pin, time in microseconds
distance= duration*0.034/2;        //Calculating actual/real distance

Serial.print("Distance = ");        //Output distance on arduino serial monitor 
Serial.println(distance);
delay(3000);                        //Pause for 3 seconds and start measuring distance again
}
