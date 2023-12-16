#include <DHT.h>
#include <DHT_U.h>
#include <Servo.h>
#include <Adafruit_Sensor.h>

#define DHT22_PIN 7

DHT dht(DHT22_PIN,  DHT22);
Servo servo;

void setup() {
  Serial.begin(9600);
  dht.begin();
  servo.attach(9);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
}

void doReading() {
  Serial.println(dht.readTemperature());
  delay(1000);
}

void loop() {
  doReading();
  while (Serial.available()) {
    char c = Serial.read();
    if (c == 'a') {
      servo.write(30);
    }
    if (c == 'b') {
      servo.write(90);
    }
  }
}
