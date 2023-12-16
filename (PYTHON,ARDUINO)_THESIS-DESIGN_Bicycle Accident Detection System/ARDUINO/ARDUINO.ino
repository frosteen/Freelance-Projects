// include the WITMOTION Sensor Library
#include <Wire.h>
#include <JY901.h>

// include the SD Library
#include <SPI.h>
#include <SD.h>
#define CS_SD 10
File file;

// include the HC05 Library
#include <SoftwareSerial.h>
SoftwareSerial AT_Serial(2, 3); // RX_OF_ARDUINO, TX_OF_ARDUINO

String filename = "Logs.txt";

void setup() {
  // Serial Monitor
  Serial.begin(9600);

  // HC05_Bluetooth
  AT_Serial.begin(38400);

  // Initiate WITMOTION Sensor
  JY901.StartIIC();

  // INITIATE SD CARD MODULE
  if (!SD.begin(CS_SD)) {
    Serial.println("SD CARD MODULE FAILED.");
    return;
  } else digitalWrite(CS_SD, LOW);

  // FILE REMOVE | UNCOMMENT IF YOU WANT TO Remove Logs.txt at STARTUP
  //  String filename = "Logs.txt";
  //  if (SD.exists(filename)) {
  //    SD.remove(filename);
  //  }
}

void loop() {
  static int cntr = 0;
  while (true) {
    // Get Data from WITMOTION Sensor
    JY901.GetTime();
    JY901.GetAcc();
    JY901.GetGyro();
    JY901.GetAngle();
    JY901.GetMag();
    cntr++;
    delay(500);
    if (cntr < 5) continue; // wait 5 seconds for stabilization
    String data = "20" + String(JY901.stcTime.ucYear) + "-" + String(JY901.stcTime.ucMonth) + "-" + String(JY901.stcTime.ucDay);
    data += " " + String(JY901.stcTime.ucHour) + ":" + String(JY901.stcTime.ucMinute) + ":" + String((float)JY901.stcTime.ucSecond + (float)JY901.stcTime.usMiliSecond / 1000);
    data += "," + String((float)JY901.stcAcc.a[0] / 32768 * 16) + "," + String((float)JY901.stcAcc.a[1] / 32768 * 16) + "," + String((float)JY901.stcAcc.a[2] / 32768 * 16);
    data += "," + String((float)JY901.stcGyro.w[0] / 32768 * 2000) + "," + String((float)JY901.stcGyro.w[1] / 32768 * 2000) + "," + String((float)JY901.stcGyro.w[2] / 32768 * 2000);
    data += "," + String((float)JY901.stcAngle.Angle[0] / 32768 * 180) + "," + String((float)JY901.stcAngle.Angle[1] / 32768 * 180) + "," + String((float)JY901.stcAngle.Angle[2] / 32768 * 180);
    data += "," + String(JY901.stcMag.h[0]) + "," + String(JY901.stcMag.h[1]) + "," + String(JY901.stcMag.h[2]);
    Serial.println(data);

    // WRITE FILE
    file = SD.open(filename, FILE_WRITE);
    if (file) {
      file.println(data);
      file.close();
    }

    // TRANSMIT to HC05
    AT_Serial.println(data);
  }
}
