#include<dht.h>

#define dht_apin 7

dht DHT;

void setup(){
  Serial.begin(9600);
}

void loop(){
  DHT.read11(dht_apin);
  Serial.print("Current temperatre:");
  Serial.println(DHT.temperature);
  delay(2000);
}
