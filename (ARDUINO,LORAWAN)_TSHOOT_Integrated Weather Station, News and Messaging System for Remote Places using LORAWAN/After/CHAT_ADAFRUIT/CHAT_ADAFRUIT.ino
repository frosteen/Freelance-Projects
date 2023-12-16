#include <DHT.h>
#include <Wire.h>
#include <SPI.h>
#include <LoRa.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <math.h>


#define SS 8
#define RST 4
#define DI0 7

#define BAND 889000000.00
#define spreadingFactor 9
#define SignalBandwidth 31.25E3
#define codingRateDenominator 8
#define preambleLength 8
#define ONE_WIRE_BUS 6
#define gas_sensor A1
#define DHTPIN 12

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DHT dht(DHTPIN, DHT11);
#define SEALEVELPRESSURE_HPA (1013.25)
Adafruit_BMP085 bme;

float ds18temp = 0;


String LoRaMessage = "";
char device_id[12] = "AWS";

String message;

byte localAddress = 0xBB;
byte destination = 0xFF;

unsigned long prevTime = millis();

void setup() {
  Serial.begin(115200);
  Wire.begin();
  dht.begin();
  sensors.begin();

  while (!Serial);
  SPI.begin();
  LoRa.setPins(SS, RST, DI0);
  Serial.println(F("LoRa Sender"));
  Serial.print("LoRa Spreading Factor: ");
  Serial.println(spreadingFactor);
  LoRa.setSpreadingFactor(spreadingFactor);
  Serial.print("LoRa Signal Bandwidth: ");
  Serial.println(SignalBandwidth);
  LoRa.setSignalBandwidth(SignalBandwidth);
  LoRa.setCodingRate4(codingRateDenominator);
  LoRa.setPreambleLength(preambleLength);

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  if (!bme.begin(0x76))
  {
    Serial.println("Could not find a valid BMP180 sensor, check wiring!");
    while (1);
  }
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - prevTime > 10000) { // every 10 seconds
    ////ANEMOMETER////

    float sensorValue = analogRead(A2);
    float voltage = (sensorValue / 1023) * 5;
    float wind_speed = mapfloat(voltage, 0.17, 5, 0, 25);
    float temperature = bme.readTemperature();
    float pressure = ((bme.readPressure() / 100.0F) - 1);
    float altitude = (bme.readAltitude() + 7 );
    float humidity = (dht.readHumidity() - 15);
    float t = ds18temp;
    double dewPoint = dewPointFast(t, humidity);
    float air_quality = analogRead(gas_sensor);
    sensors.requestTemperatures();
    ds18temp = (sensors.getTempCByIndex(0));


    if (voltage < 0.17)
    {
      float wind_speed = 0;
      // Serial.print("Wind Speed =");
      // Serial.print(wind_speed);
      //Serial.println("m/s");

    }

    if (voltage >= 0.17)
    {

    }


    LoRaMessage = String(device_id) + "/" + String(ds18temp) + "&" + String(pressure)
                  + "#" + String(altitude) + "@" + String(humidity) + "$" + String(dewPoint)
                  + "^" + String(air_quality) + "!" + String(wind_speed); //+ "!" + /String(lux);

    LoRa.beginPacket();
    LoRa.print(LoRaMessage);
    LoRa.endPacket();
    Serial.println(LoRaMessage);

    //  Serial.println();
    prevTime = currentTime;
  }

  while (Serial.available()) {
    delay(2);  //delay to allow byte to arrive in input buffer
    char c = Serial.read();
    message += c;
  }

  if (message.length() > 0) {
    Serial.println("Mateo: " + message); //name seen in the Serial Monitor
    LoRa.beginPacket();
    LoRa.write(destination);
    LoRa.write(localAddress);
    LoRa.println("Mateo: " + message); //name seen on the receiving end
    LoRa.endPacket();
    message = "";
  }



  // send packet
  //LoRa.beginPacket();
  //LoRa.endPacket();
  onReceive(LoRa.parsePacket());


}

void onReceive(int packetSize) {
  if (packetSize == 0) return;          // if there's no packet, return

  int recipient = LoRa.read();
  String incoming = "";

  while (LoRa.available()) {
    incoming += (char)LoRa.read();
  }

  //  if (recipient != localAddress && recipient != 0xBB) {
  //    Serial.println("This message is not for me.");
  //    return;                             // skip rest of function
  //  }

  Serial.print(incoming);
  Serial.print(" || RSSI: ");
  Serial.print(LoRa.packetRssi());
  Serial.println();
}

double dewPointFast(double celsius, double humidity)
{
  double a = 17.271;
  double b = 237.7;
  double temp = ((a * celsius) / (b + celsius) + log(humidity * 0.01));
  double Td = ((b * temp) / (a - temp));

  return Td;
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
////SENSORS////////