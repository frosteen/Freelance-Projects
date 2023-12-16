#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <MPU6050.h>


MPU6050 mpu;

int SCL_PIN = D1;
int SDA_PIN = D2;

void doGPS();


SoftwareSerial serial(D7, D8); //Rx, Tx
#define FIREBASE_HOST "tracksoldiers-870ba.firebaseio.com"
#define FIREBASE_AUTH "Ug7mox60P5qFV8jd8kCBeqosqBu8qDlJe1h6GLUM"

void setup() {
  Serial.begin(9600);
  serial.begin(9600);
  pinMode(D6, OUTPUT);
  digitalWrite(D6, LOW);
  String wifi[2];
  int counter = 0;
  while (1) {
    if (serial.available()) {
      char c = serial.read();
      if (c != '&') {
        wifi[counter] += c;
      }
      else if (counter != 1) {
        serial.read();
        counter += 1;
      } else {
        break;
      }
    }
    yield();
  }
  // connect to wifi.
  //  WiFi.begin();
  Serial.println();
  Serial.print("WIFINAME:");
  Serial.println(wifi[0]);
  Serial.print("WIFIPASS:");
  Serial.println(wifi[1]);
  char wifi0[20];
  char wifi1[20];
  wifi[0].toCharArray(wifi0, 20);
  wifi[1].toCharArray(wifi1, 20);
  Serial.print("WIFINAME:");
  Serial.println(wifi0);
  Serial.print("WIFIPASS:");
  Serial.println(wifi1);
  WiFi.begin(wifi0, wifi1);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  while (!mpu.beginSoftwareI2C(SCL_PIN, SDA_PIN, MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  serial.print("A");
  doGPS();
  //INDICATORS FINISHED
  serial.print("B");
  digitalWrite(D6, HIGH);
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}


#define pulsePin A0

int rate[10];
unsigned long sampleCounter = 0;
unsigned long lastBeatTime = 0;
unsigned long lastTime = 0, N;
int BPM = 0;
int IBI = 0;
int P = 512;
int T = 512;
int thresh = 512;
int amp = 100;
int Signal;
boolean Pulse = false;
boolean firstBeat = true;
boolean secondBeat = true;
boolean QS = true;

void readPulse() {

  Signal = analogRead(pulsePin);
  sampleCounter += 2;
  int N = sampleCounter - lastBeatTime;

  detectSetHighLow();

  if (N > 5) {
    if ( (Signal > thresh) && (Pulse == false) && (N > (IBI / 5) * 3) )
      pulseDetected();
  }

  if (Signal < thresh && Pulse == true) {
    Pulse = false;
    amp = P - T;
    thresh = amp / 2 + T;
    P = thresh;
    T = thresh;
  }

  if (N > 2500) {
    thresh = 512;
    P = 512;
    T = 512;
    lastBeatTime = sampleCounter;
    firstBeat = true;
    secondBeat = true;
  }

}

void detectSetHighLow() {

  if (Signal < thresh && N > (IBI / 5) * 3) {
    if (Signal < T) {
      T = Signal;
    }
  }

  if (Signal > thresh && Signal > P) {
    P = Signal;
  }

}

void pulseDetected() {
  Pulse = true;
  IBI = sampleCounter - lastBeatTime;
  lastBeatTime = sampleCounter;

  if (firstBeat) {
    firstBeat = false;
    return;
  }
  if (secondBeat) {
    secondBeat = false;
    for (int i = 0; i <= 9; i++) {
      rate[i] = IBI;
    }
  }

  word runningTotal = 0;

  for (int i = 0; i <= 8; i++) {
    rate[i] = rate[i + 1];
    runningTotal += rate[i];
  }

  rate[9] = IBI;
  runningTotal += rate[9];
  runningTotal /= 10;
  BPM = 60000 / runningTotal;
  QS = true;
}

float timeStep = 0.01;


float pitchG = 0;
float rollG = 0;
float yawG = 0;

const char* Host = "www.unwiredlabs.com";
String endpoint = "/v2/process.php";

// UnwiredLabs API_Token. Signup here to get a free token https://unwiredlabs.com/trial
String token = "cf5c1d64919b3b";

String jsonString = "{\n";

// Variables to store unwiredlabs response
double latitude = 0;
double longitude = 0;
double accuracy = 0;
String address = "";

int counter69 = 0;

void doGPS() {
  char bssid[6];
  DynamicJsonBuffer jsonBuffer;

  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("scan done");

  if (n == 0 ) {
    Serial.println("No networks available");
  } else {
    Serial.print(n);
    Serial.println(" networks found");
  }

  // now build the jsonString...
  jsonString = "{\n";
  jsonString += "\"token\" : \"";
  jsonString += token;
  jsonString += "\",\n";
  jsonString += "\"id\" : \"saikirandevice01\",\n";
  jsonString += "\"wifi\": [\n";
  for (int j = 0; j < n; ++j) {
    jsonString += "{\n";
    jsonString += "\"bssid\" : \"";
    jsonString += (WiFi.BSSIDstr(j));
    jsonString += "\",\n";
    jsonString += "\"signal\": ";
    jsonString += WiFi.RSSI(j);
    jsonString += "\n";
    if (j < n - 1) {
      jsonString += "},\n";
    } else {
      jsonString += "}\n";
    }
  }
  jsonString += ("]\n");
  jsonString += ("}\n");
  Serial.println(jsonString);

  WiFiClientSecure client;

  //Connect to the client and make the api call
  Serial.println("Requesting URL: https://" + (String)Host + endpoint);
  if (client.connect(Host, 443)) {
    Serial.println("Connected");
    client.println("POST " + endpoint + " HTTP/1.1");
    client.println("Host: " + (String)Host);
    client.println("Connection: close");
    client.println("Content-Type: application/json");
    client.println("User-Agent: Arduino/1.0");
    client.print("Content-Length: ");
    client.println(jsonString.length());
    client.println();
    client.print(jsonString);
    delay(500);
  }

  //Read and parse all the lines of the reply from server
  while (client.available()) {
    String line = client.readStringUntil('\r');
    JsonObject& root = jsonBuffer.parseObject(line);
    if (root.success()) {
      latitude    = root["lat"];
      longitude   = root["lon"];
      accuracy    = root["accuracy"];

      Serial.println();
      Serial.print("Latitude = ");
      Serial.println(latitude, 6);
      Serial.print("Longitude = ");
      Serial.println(longitude, 6);
      Serial.print("Accuracy = ");
      Serial.println(accuracy);
    }
  }

  Serial.println("closing connection");
  Serial.println();
  client.stop();
}

void loop() {
  counter69 += 1;
  Firebase.setString("LONGITUDE", String(longitude));
  Firebase.setString("LATITUDE", String(latitude));
  Firebase.setString("ACCURACY", String(accuracy));
  if (counter69 >= 20 * 60 * 1000) {
    counter69 = 0;
    doGPS();
  }
  //HEARTBEAT//
  if (QS == true) {
    Firebase.setString("BPM", String(BPM));
    QS = false;
  } else if (millis() >= (lastTime + 2)) {
    readPulse();
    lastTime = millis();
  }
  //MPU//

  //ACCELERATION
  Vector normAccel = mpu.readNormalizeAccel();
  int pitch = -(atan2(normAccel.XAxis, sqrt(normAccel.YAxis * normAccel.YAxis + normAccel.ZAxis * normAccel.ZAxis)) * 180.0) / M_PI;
  int roll = (atan2(normAccel.YAxis, normAccel.ZAxis) * 180.0) / M_PI;
  Firebase.setString("APITCH", String(pitch));
  Firebase.setString("AROLL", String(roll));

  //GYROSCOPE
  Vector norm = mpu.readNormalizeGyro();
  pitchG = pitchG + norm.YAxis * timeStep;
  rollG = rollG + norm.XAxis * timeStep;
  yawG = yawG + norm.ZAxis * timeStep;
  Firebase.setString("GPITCH", String(pitchG));
  Firebase.setString("GROLL", String(rollG));
  Firebase.setString("GYAW", String(yawG));

  //TEMPERATURE
  float temp = mpu.readTemperature();
  String formatTemp = String(temp) + " *C";
  Firebase.setString("TEMPERATURE", String(formatTemp));
}
