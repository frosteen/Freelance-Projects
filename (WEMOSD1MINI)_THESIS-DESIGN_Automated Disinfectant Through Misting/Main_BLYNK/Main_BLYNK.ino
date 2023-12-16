// Device Details
#define BLYNK_TEMPLATE_ID "TMPLpQvLWDf_"
#define BLYNK_DEVICE_NAME "Design Misting"
#define BLYNK_AUTH_TOKEN "38_nnjkDxoAsPEVSyIkVBa096y_YFu7y"

// Libraries
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <DHT.h>

// Credentials
char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "PLDTHOMEFIBRb4138";
char pass[] = "pldtWIFI25**";

// Pins
#define MISTING_PIN D1
#define DHT11_PIN D2
#define LED_PIN LED_BUILTIN

// DHT Settings
float humidity_scale = 0.9375; // SLOPE
float humidity_offset = 2.3125; // OFFSET

// Variables
bool is_auto = false;
float humidity_threshold = 0;
float current_humidity = 0;
int debounce = 0;

// Motor
int x = 0;
int y = 0;
int min_range = 0;
int max_range = 100;
#define in1 D5
#define in2 D6
#define in3 D7
#define in4 D8

// FUNCTIONS
void check_humidity();
void auto_mist();
void move_control();

// Initialize DHT
DHT dht(DHT11_PIN, DHT22);

void setup()
{
  // Define PINS
  pinMode(LED_PIN, OUTPUT);
  pinMode(MISTING_PIN, OUTPUT);
  digitalWrite(MISTING_PIN, HIGH);

  // Reset Switching
  digitalWrite(MISTING_PIN, LOW);
  delay(200);
  digitalWrite(MISTING_PIN, HIGH);

  // Debug console
  Serial.begin(9600);

  // Blynk begin
  Blynk.begin(auth, ssid, pass);

  // DHT begin
  dht.begin();

  // MOTOR
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}

void loop()
{
  Blynk.run();
  check_humidity();
  auto_mist();
}

void switch_misting(int switch_mode)
{
  if (switch_mode == 0 && debounce == 0) {
    digitalWrite(MISTING_PIN, LOW);
    delay(200);
    digitalWrite(MISTING_PIN, HIGH);
    debounce = 1;
  } else if (switch_mode == 1 && debounce == 1) {
    digitalWrite(MISTING_PIN, LOW);
    delay(200);
    digitalWrite(MISTING_PIN, HIGH);
    debounce = 0;
  }
}

void check_humidity()
{
  float h = dht.readHumidity();
  if (!isnan(h))
    current_humidity = h * humidity_scale + humidity_offset;
  // Testing Purposes
  //  current_humidity += 0.1;
  //  if (current_humidity > 80)
  //    current_humidity = 0;
  Serial.print(F("Current Humidity: "));
  Serial.println(current_humidity);
  Blynk.virtualWrite(V3, current_humidity);
}

void auto_mist()
{
  if (is_auto)
  {
    if (current_humidity <= humidity_threshold) {
      switch_misting(1);
      digitalWrite(LED_PIN, LOW);
    } else {
      switch_misting(0);
      digitalWrite(LED_PIN, HIGH);
    }
    Blynk.virtualWrite(V1, 1);
  }
}

void move_control()
{
  int median = (max_range + min_range) / 2;
  int lower = median - median / 1.5;
  int upper = median + median / 1.5;

  // Move Forward
  if (x > lower && x < upper && y >= upper && y <= max_range)
  {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }

  // Move Right
  if (y > lower && y < upper && x >= upper && x <= max_range)
  {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }

  // Move Backward
  if (x > lower && x < upper && y >= min_range && y <= lower)
  {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  }

  // Move Left
  if (y > lower && y < upper && x >= min_range && x <= lower)
  {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  }

  // Stop
  if (x == median && y == median)
  {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
  }
}

// Auto Misting
BLYNK_WRITE(V0)
{
  if (param.asInt() == 0)
  {
    is_auto = false;
    Blynk.syncVirtual(V1);
  } else {
    is_auto = true;
  }
}

// Enable Misting (Manual)
BLYNK_WRITE(V1)
{
  if (!is_auto) {
    switch_misting(param.asInt());
    digitalWrite(LED_PIN, !param.asInt());
  }
}

// Humidity Threshold
BLYNK_WRITE(V2)
{
  humidity_threshold = param.asInt();
}

// JoystickX
BLYNK_WRITE(V4)
{
  x = param.asInt();
  move_control();
}

// JoystickY
BLYNK_WRITE(V5)
{
  y = param.asInt();
  move_control();
}

BLYNK_CONNECTED()
{
  Blynk.syncAll();
}
