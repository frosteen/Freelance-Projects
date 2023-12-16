// TEMPLATE
#define BLYNK_TEMPLATE_ID "TMPL6NSnaQYvp"
#define BLYNK_TEMPLATE_NAME "Water Irrigation System"
#define BLYNK_AUTH_TOKEN "3zocUTmfUJFN-ZSmXPCC3NDo3EtOmXP9"

// LIBRARIES
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <Wire.h>
#include <BH1750.h>
#include "ADS1X15.h"

// SPRINKLER TIMER
const int irradiance_sprinkler_timer = 30;  // seconds

// IRRADIANCE CHECKING INTERVAL;
const int irradiance_check_interval = 30;  // seconds

// HOTSPOT CREDENTIALS
char ssid[] = "mapua-water-irrigation-system";
char pass[] = "mwis2023";

// ENABLE AUTOMATION
bool is_automated = true;

// PINS
const int moisture_pin = A0;
const int sprinkler_pin = D3;

// OBJECTS
BH1750 light_meter;
ADS1115 ADS(0x48);

// THRESHOLDS
float moisture_thresh_low = 0;
float moisture_thresh_high = 0;
float irradiance_thresh_low = 0;
float irradiance_thresh_high = 0;

// ONCE BLYNK CONNECTED SYNC
BLYNK_CONNECTED() {
  Blynk.syncAll();
}

// MOISTURE THRESHOLD
BLYNK_WRITE(V2) {
  moisture_thresh_low = param.asInt();
}
BLYNK_WRITE(V3) {
  moisture_thresh_high = param.asInt();
}

// IRRADIANCE THRESHOLD
BLYNK_WRITE(V4) {
  irradiance_thresh_low = param.asFloat();
}
BLYNK_WRITE(V5) {
  irradiance_thresh_high = param.asFloat();
}

// MANUAL SPRINKLER
BLYNK_WRITE(V8) {
  if (!is_automated) {
    int value = !param.asInt();
    digitalWrite(sprinkler_pin, value);
  }
}

// RUN EVERY
boolean run_every(unsigned long interval) {
  static unsigned long previousMillis = 0;
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    return true;
  }
  return false;
}

// CYCLE CHECK
boolean cycle_check(unsigned long *last_millis, unsigned long cycle) {
  unsigned long current_millis = millis();
  if (current_millis - *last_millis >= cycle) {
    *last_millis = current_millis;
    return true;
  }
  return false;
}


// CHECKER FUNCTIONS
void voltage_and_current_check() {
  ADS.setGain(0);
  float voltage_adc = ADS.readADC(0);
  float current_voltage_adc = ADS.readADC(1);
  float factor = ADS.toVoltage(1);

  float voltage = voltage_adc * factor * 5;
  float current_voltage = current_voltage_adc * factor;
  float current = ((current_voltage)-2.25) / 0.185;

  Serial.println(current_voltage);

  String voltage_and_current = String(voltage) + "V" + "  " + String(current) + "A";

  Serial.println(voltage_and_current);
  Blynk.virtualWrite(V0, voltage_and_current);
}
void soil_check() {
  // STATIC VAR
  static bool first_run = true;
  static bool activated_by_irradiance = false;
  static unsigned long last_millis = 0;

  // GET SOIL MOISTURE
  float moisture = analogRead(moisture_pin);
  Blynk.virtualWrite(V6, moisture);

  // GET SOIL IRRADIANCE
  float lux = light_meter.readLightLevel();
  float irr = (lux * 0.0079);
  Blynk.virtualWrite(V7, irr);

  if (is_automated) {
    // Check MOISTURE Thresholds
    if (moisture_thresh_low <= moisture && moisture <= moisture_thresh_high && !activated_by_irradiance) {
      activate_sprinker(true);
    } else if (!activated_by_irradiance) {
      activate_sprinker(false);
    }
    
    // Check IRRADIANCE Thresholds
    if (run_every(irradiance_check_interval * 1000) || first_run) {
      if (irradiance_thresh_low <= irr && irr <= irradiance_thresh_high && !activated_by_irradiance) {
        activate_sprinker(true);
        activated_by_irradiance = true;
        first_run = false;
        last_millis = millis();
      }
    }
    // STOP SPRINKLER WHEN REACHES TIMER
    if (cycle_check(&last_millis, irradiance_sprinkler_timer * 1000) && activated_by_irradiance) {
      activate_sprinker(false);
      activated_by_irradiance = false;
    }
  }
}

// ACTIVATE SPRINKLER
void activate_sprinker(bool is_activate) {
  if (is_activate) {
    Blynk.virtualWrite(V8, 1);
    digitalWrite(sprinkler_pin, 0);
  } else {
    Blynk.virtualWrite(V8, 0);
    digitalWrite(sprinkler_pin, 1);
  }
}

void setup() {
  // PINMODE
  pinMode(sprinkler_pin, OUTPUT);

  // INITIATE SERIAL MONITOR and I2C
  Serial.begin(115200);
  // USES I2C
  Wire.begin();
  light_meter.begin();
  ADS.begin();

  // INITIATE BLYNK
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  Serial.println(F("CONNECTED!"));
}

void loop() {
  Blynk.run();
  soil_check();
  voltage_and_current_check();
}
