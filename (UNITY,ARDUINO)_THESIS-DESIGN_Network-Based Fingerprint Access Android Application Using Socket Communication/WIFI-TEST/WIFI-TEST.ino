#include <ESP8266WiFi.h>

const char* ssid = "Cisco45549";
const char* password = "";

WiFiServer server(5001);

void setup()
{
  Serial.begin(115200);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  IPAddress ip(192, 168, 1, 200);
  IPAddress gateway(192, 168, 1, 1);
  IPAddress subnet(255, 255, 255, 0);
  WiFi.config(ip, gateway, subnet);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
  Serial.println(WiFi.localIP());
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
