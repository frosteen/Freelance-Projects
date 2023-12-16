#include <ESP8266WiFi.h>

const char* ssid = "ESP8266TEST";
const char* password = "thereisnospoon";

WiFiServer server(5001);

void setup()
{
  Serial.begin(115200);
  Serial.println();

  Serial.printf("Configuring:  %s", ssid);
  WiFi.softAP(ssid, password);
  Serial.println("");
  Serial.print("IP address:\t");
  Serial.println(WiFi.softAPIP());     
  server.begin();
}


void loop() {
  WiFiClient client = server.available();
  if (client) { //if there is a client
    while (Serial.available()) {
      String text = Serial.readStringUntil('\n');
      client.println(text);
    }
  }
}
