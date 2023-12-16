#include <DHT.h>
#include <DHT_U.h>


#define DHT11_PIN D0

DHT dht(DHT11_PIN,  DHT11);


void setup() {
  Serial.begin(9600);
  dht.begin();
}


void doReading() {
  Serial.println(dht.readTemperature());
  delay(1000);
}

void loop() {
  doReading();
}
