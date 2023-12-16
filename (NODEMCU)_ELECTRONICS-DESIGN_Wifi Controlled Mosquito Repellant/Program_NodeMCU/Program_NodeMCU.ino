#define BLYNK_TEMPLATE_ID "TMPL9z8ICtRY"
#define BLYNK_DEVICE_NAME "WIFI Controlled Mosquito Repellant"
#define BLYNK_AUTH_TOKEN            "FPKh-TgKZ0ZpSxiXmHpcApR7V5KfaPv8"

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

int buzzer_pin = D1;

int freq;
bool is_on = false;

char auth[] = BLYNK_AUTH_TOKEN;

char ssid[] = "FREE WIFI";
char pass[] = "aplnjjndt";

BLYNK_WRITE(V0)
{
  int value = param.asInt();

  if (value == 1) {
    is_on = true;
    Blynk.syncVirtual(V1);
  } else {
    noTone(buzzer_pin);
    is_on = false;
  }
}

BLYNK_WRITE(V1)
{
  freq = param.asInt();
  if (is_on == true) {
    tone(buzzer_pin, freq);
  } else {
    noTone(buzzer_pin);
  }
}

BLYNK_CONNECTED() {
  Blynk.syncVirtual(V0);
}

void setup()
{
  pinMode(buzzer_pin, OUTPUT);
  Serial.begin(115200);
  Blynk.begin(auth, ssid, pass);
}

void loop()
{
  Blynk.run();
}
