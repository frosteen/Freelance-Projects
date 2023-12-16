#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <PID_v1.h>
#define DHT22_PIN 8
#define pwm  9

int fanSpeedPercentage = 0;
char mode = 'A';
double pwmValue = 0;


DHT dht(DHT22_PIN,  DHT22);

void setup() {
  Serial.begin(9600);
  dht.begin();
  analogWrite(pwm, 0);
}

void loop() {
  double temp = dht.readTemperature();
  if (mode == 'A') {
    pwmValue = map(temp*100, 2600, 3200, 0, 255);
    analogWrite(pwm, pwmValue);
  } else if (mode == 'B') {
    pwmValue = 255*fanSpeedPercentage/100;
    analogWrite(pwm, pwmValue);
  }
  if (Serial.available() > 0) {
    mode = (char)Serial.read();
    if (mode == 'B') {
      fanSpeedPercentage = Serial.parseInt();
    }
  }
  Serial.println(String(temp)+";"+String(pwmValue/255*100));
  delay(1000);
}

