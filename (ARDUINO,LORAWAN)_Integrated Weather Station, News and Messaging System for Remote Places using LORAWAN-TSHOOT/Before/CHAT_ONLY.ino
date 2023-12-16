#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>

#define SS 8
#define RST 4
#define DI0 7

#define BAND 889000000.00
#define spreadingFactor 9
#define SignalBandwidth 31.25E3
#define codingRateDenominator 8
#define preambleLength 8

String message;

byte localAddress = 0xBB;  
byte destination = 0xFF;

void setup() {
  Wire.begin();
  Serial.begin(250000);
  Serial.println("LoRa message service");

  
  while (!Serial);
  SPI.begin();
  LoRa.setPins(SS, RST, DI0);
  LoRa.setSpreadingFactor(spreadingFactor);
  LoRa.setSignalBandwidth(SignalBandwidth);
  LoRa.setCodingRate4(codingRateDenominator);
  LoRa.setPreambleLength(preambleLength);
  
  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  delay(1000);
}

void loop() {
  while (Serial.available()) {
    delay(2);  //delay to allow byte to arrive in input buffer
    char c = Serial.read();
    message += c;
  }

  if (message.length() > 0) {
    Serial.println("Alvin: " + message); //name seen in the Serial Monitor
    LoRa.beginPacket();
    LoRa.write(destination);              
    LoRa.write(localAddress);
    LoRa.print("Alvin: " + message); //name seen on the receiving end
    LoRa.endPacket();
    message = "";
  }

  onReceive(LoRa.parsePacket());

}

void onReceive(int packetSize) {
  if (packetSize == 0) return;          // if there's no packet, return

  int recipient = LoRa.read();
  String incoming = "";

  while (LoRa.available()) {
    incoming += (char)LoRa.read();
  }

  if (recipient != localAddress && recipient != 0xFF) {
    Serial.println("This message is not for me.");
    return;                             // skip rest of function
  }

  Serial.print(incoming);
  Serial.print(" || RSSI: ");
  Serial.println(LoRa.packetRssi());
  Serial.println();
}