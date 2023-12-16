
#include <ESP8266WiFi.h>
#include <time.h>

#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>

// Set these to run example.
#define FIREBASE_HOST "trafficcounter-915f7.firebaseio.com"
#define FIREBASE_AUTH "q7ZxHJowI2IlT5Km05hoDdzUuXyX50BBTwQ6ECMo"

const char* ssid = "tcounter";
const char* password = "tcounter";

int timezone = 8 * 3600;
int dst = 0;

int threshold = 60; //change to 140

void setup() {

  pinMode(D1,OUTPUT);
  digitalWrite(D1, LOW);

  Serial.begin(9600);
  Serial.println();
  Serial.print("Wifi connecting to ");
  Serial.println( ssid );

  WiFi.begin(ssid, password);

  Serial.println();

  Serial.print("Connecting");

  while ( WiFi.status() != WL_CONNECTED ) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("Wifi Connected Success!");
  Serial.print("NodeMCU IP Address : ");
  Serial.println(WiFi.localIP() );

  configTime(timezone, dst, "pool.ntp.org", "time.nist.gov");
  Serial.println("\nWaiting for Internet time");

  while (!time(nullptr)) {
    Serial.print("*");
    delay(1000);
  }
  Serial.println("\nTime response....OK");
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  delay(3000);
  Serial.println("READY");
  digitalWrite(D1, HIGH);
}
int cntr = 0;
void loop() {
  //TIME
  time_t now = time(nullptr);
  struct tm* p_tm = localtime(&now);
  Serial.println(analogRead(A0) );
  if (analogRead(A0) >= threshold) {
    cntr++;
    Serial.println("PRESSED");
    while (analogRead(A0) >= threshold) {
      yield();
    }
  }
  if (cntr == 2) {
    Serial.println("RECORDED");
    Firebase.setString("TRAFFIC/"+String(p_tm->tm_mon+1)+"~"+String(p_tm->tm_mday)+"~"+String(p_tm->tm_year + 1900)+"/"+String(p_tm->tm_hour) + ":" + String(p_tm->tm_min) + ":" + String(p_tm->tm_sec), "RECORDED");
    cntr = 0;
  }
  delay(10);

}
