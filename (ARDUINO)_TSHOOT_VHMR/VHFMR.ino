m// VHF Marine Radio

#include <DHT.h> // DHT11 Library

#include <TinyGPS++.h> // GPS Library

// OLED Libraries
#include <SPI.h>
#include <Wire.h> // I2C Communication
#include <Adafruit_GFX.h> // Graphic Display
#include <Adafruit_SSD1306.h> // Driver

#include <SoftwareSerial.h> // Multiple Serial Library

// Definitions
# define BATTERY_OUT A1

# define DHT11_OUT 1

#define VHF_TX 2
#define VHF_RX 3
#define GPS_TX 4
#define GPS_RX 5
#define GSM_TX 6
#define GSM_RX 7

#define VHF_PTT 8
#define VHF_PD 9

#define TACT_SWITCH_PTT 10
#define TACT_SWITCH_BACK 11
#define TACT_SWITCH_SELECT 12
#define TACT_SWITCH_NEXT 13

#define TIMEOUT 50

#define SCREEN_HEIGHT 64
#define SCREEN_WIDTH 128

DHT HT(DHT11_OUT,DHT11); // DHT11 Configuration

TinyGPSPlus GPS; // TinyGPS Configuration

Adafruit_SSD1306 display(SCREEN_WIDTH,SCREEN_HEIGHT,&Wire,-1); // OLED Configuration

// Serial Configuration
SoftwareSerial serialVHF(VHF_RX,VHF_TX);
SoftwareSerial serialGPS(GPS_RX,GPS_TX);
SoftwareSerial serialGSM(GSM_RX,GSM_TX);

// Global Variables

int menuHome = 1;
int menuVHF = 2;
int subHome = 1;
int subVHF = 1;

float bandwidth[2] = {12.5000, 25.0000};
int indexBandwidth = 0;

int TX_Frequency_Tens = 3;
int TX_Frequency_Units = 4;
int TX_Frequency_Tenths = 0;
int TX_Frequency_Hundredths = 0;

int RX_Frequency_Tens = 3;
int RX_Frequency_Units = 4;
int RX_Frequency_Tenths = 0;
int RX_Frequency_Hundredths = 0;

int TX_CTCSS_Tens = 0;
int TX_CTCSS_Units = 0;

int RX_CTCSS_Tens = 0;
int RX_CTCSS_Units = 0;

int squelch = 0;
int volume = 8;

String VHF_PTT_State;

String GPS_Latitude;
String GPS_Longitude;

unsigned long startMillis;
unsigned long currentMillis;
const unsigned long period = 300*1e3; // EVERY 5 MINUTES

String GSM_Number = "+639563022737"; // DEVICE 1

void setup() {
  
  // OLED Configuration
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  
  // DHT11 Configuration
  HT.begin();
  
  // GSM Configuration (Every 5 Minutes)
  startMillis = millis();
  
  // Serial Configuration
  serialVHF.begin(9600);
  serialGPS.begin(9600);
  serialGSM.begin(9600);
  
  // VHF Configuration
  pinMode(VHF_PTT,OUTPUT);
  pinMode(VHF_PD,OUTPUT);
  digitalWrite(VHF_PTT,HIGH); // HIGH: RECEIVE MODE
  digitalWrite(VHF_PD,HIGH);
  
  // Pin Mode
  pinMode (BATTERY_OUT,INPUT);
  
  pinMode(TACT_SWITCH_PTT,INPUT);
  pinMode(TACT_SWITCH_BACK,INPUT);
  pinMode(TACT_SWITCH_SELECT,INPUT);
  pinMode(TACT_SWITCH_NEXT,INPUT);
}

void loop() {
  
  switch(subHome) {
    case 0:
    subHome = 1;
    break;
    case 1:
    currentMillis = millis();
    
    if (currentMillis - startMillis >= period) {
      sendMessageGSM();
      startMillis = currentMillis;
    }
    
    switchHome();
    updateHome();
    break;
    case 2:
    displayAmbience();
    switchBackHome();
    break;
    case 3:
    displayCompass();
    switchBackHome();
    break;
    case 4:
    displayGPS();
    switchBackHome();
    break;
    
    case 5:
    switchPTT();
    
    switch(subVHF) {
    case 0:
    subVHF = 1;
    break;
    case 1:
    switchVHF();
    updateVHF();
    break;
    case 2:
    editBandwidth();
    switchBandwidth();
    switchBackVHF();
    break;
    case 3:
    editTX_Frequency_Tens();
    switchTX_Frequency_Tens();
    switchBackVHF();
    break;
    case 4:
    editTX_Frequency_Units();
    switchTX_Frequency_Units();
    switchBackVHF();
    break;
    case 5:
    editTX_Frequency_Tenths();
    switchTX_Frequency_Tenths();
    switchBackVHF();
    break;
    case 6:
    editTX_Frequency_Hundredths();
    switchTX_Frequency_Hundredths();
    switchBackVHF();
    break;
    case 7:
    editRX_Frequency_Tens();
    switchRX_Frequency_Tens();
    switchBackVHF();
    break;
    case 8:
    editRX_Frequency_Units();
    switchRX_Frequency_Units();
    switchBackVHF();
    break;
    case 9:
    editRX_Frequency_Tenths();
    switchRX_Frequency_Tenths();
    switchBackVHF();
    break;
    case 10:
    editRX_Frequency_Hundredths();
    switchRX_Frequency_Hundredths();
    switchBackVHF();
    break;
    case 11:
    editTX_CTCSS_Tens();
    switchTX_CTCSS_Tens();
    switchBackVHF();
    break;
    case 12:
    editTX_CTCSS_Units();
    switchTX_CTCSS_Units();
    switchBackVHF();
    break;
    case 13:
    editRX_CTCSS_Tens();
    switchRX_CTCSS_Tens();
    switchBackVHF();
    break;
    case 14:
    editRX_CTCSS_Units();
    switchRX_CTCSS_Units();
    switchBackVHF();
    break;
    case 15:
    editSquelch();
    switchSquelch();
    switchBackVHF();
    break;
    case 16:
    editVolume();
    switchVolume();
    switchBackVHF();
    break;
    case 17:
    subVHF = 16;
    break;
    }
    break;
    
    case 6:
    subHome = 5;
    break;
  }
}

void battery() {
  
  displayTextSettings();
  
  display.drawRect(100,0,20,5,WHITE);
  display.fillRect(100,0,analogRead(A0)*359. / 1023.,5,WHITE);
  
  display.display();
}

void blinkText() {
  
  for(int i=0; i<2; i++) {
    if(i>0){
      display.display();
    }
  }
}

void switchHome() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    menuHome--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    menuHome++;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_SELECT)) {
    executeHome();
  }
}

void switchVHF() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    menuVHF--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    menuVHF++;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_SELECT)) {
    executeVHF();
    
    //handshakeVHF();
    //setGroupVHF();
    //setVolumeVHF();
  }
}

void switchBandwidth() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    indexBandwidth--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    indexBandwidth++;
    delay(200);
  }
  
  if (indexBandwidth < 0) {
    indexBandwidth = 0; // Minimum
  }
  if (indexBandwidth > 1) {
    indexBandwidth = 1; // Maximum
  }
}

void switchTX_Frequency_Tens() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    TX_Frequency_Tens--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    TX_Frequency_Tens++;
    delay(200);
  }
  
  if (TX_Frequency_Tens < 3) {
    TX_Frequency_Tens = 3; // Minimum
  }
  if (TX_Frequency_Tens > 7) {
    TX_Frequency_Tens = 7; // Maximum
  }
  // Ex. 1X5, X will be 6. (165)
  if (TX_Frequency_Units > 4) {
    if (TX_Frequency_Tens > 6) {
      TX_Frequency_Tens = 6;
    }
  }
  // Ex. 1X3, X will be 4. (144)
  if (TX_Frequency_Units < 4) {
    if (TX_Frequency_Tens < 4) {
      TX_Frequency_Tens = 4;
    }
  }
  // Case: 1X4.1125, X will be 6. (164.1125)
  if ((TX_Frequency_Tenths > 0 || TX_Frequency_Hundredths > 0) & TX_Frequency_Units > 3) {
    if (TX_Frequency_Tens > 6) {
      TX_Frequency_Tens = 6;
    }
  }
}

void switchTX_Frequency_Units() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    TX_Frequency_Units--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    TX_Frequency_Units++;
    delay(200);
  }
  
  if (TX_Frequency_Units < 0) {
    TX_Frequency_Units = 0; // Minimum
  }
  if (TX_Frequency_Units > 9) {
    TX_Frequency_Units = 9; // Maximum
  }
  
  switch(TX_Frequency_Tens) {
    case 3: // Case: 13X
    if (TX_Frequency_Units < 4) {
      TX_Frequency_Units = 4; // Minimum
    }
    if (TX_Frequency_Units > 9) {
      TX_Frequency_Units = 9; // Maximum
    }
    break;
    case 7: // Case: 17X
    if (TX_Frequency_Units < 0) {
      TX_Frequency_Units = 0; // Minimum
    }
    if (TX_Frequency_Units > 4) {
      TX_Frequency_Units = 4; // Maximum
    }
    break;
  }
  // Case: 17X.1125, X will be 3. (173.1125)
  if ((TX_Frequency_Tenths > 0 || TX_Frequency_Hundredths > 0) & TX_Frequency_Tens > 6) {
    if (TX_Frequency_Units > 3) {
      TX_Frequency_Units = 3;
    }
  }
}

void switchTX_Frequency_Tenths() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    TX_Frequency_Tenths--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    TX_Frequency_Tenths++;
    delay(200);
  }
  
  if (TX_Frequency_Tenths < 0) {
    TX_Frequency_Tenths = 0; // Minimum
  }
  if (TX_Frequency_Tenths > 9) {
    TX_Frequency_Tenths = 9; // Maximum
  }
  // Case: 174.X000, X will be 0. (174.0000)
  if (TX_Frequency_Tens == 7 & TX_Frequency_Units == 4) {
    TX_Frequency_Tenths = 0;
  }
}

void switchTX_Frequency_Hundredths() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    TX_Frequency_Hundredths = TX_Frequency_Hundredths - bandwidth[indexBandwidth]*10;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    TX_Frequency_Hundredths = TX_Frequency_Hundredths + bandwidth[indexBandwidth]*10;
    delay(200);
  }
  
  if (TX_Frequency_Hundredths < 0) {
    TX_Frequency_Hundredths = 0; // Minimum
  }
  if (TX_Frequency_Hundredths > 875) {
    TX_Frequency_Hundredths = 875; // Maximum
  }
  // Case: 174.0X, X will be 0. (174.0000)
  if (TX_Frequency_Tens == 7 & TX_Frequency_Units == 4) {
    TX_Frequency_Hundredths = 0;
  }
}

void switchRX_Frequency_Tens() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    RX_Frequency_Tens--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    RX_Frequency_Tens++;
    delay(200);
  }
  
  if (RX_Frequency_Tens < 3) {
    RX_Frequency_Tens = 3;
  }
  if (RX_Frequency_Tens > 7) {
    RX_Frequency_Tens = 7;
  }
  
  if (RX_Frequency_Units > 4) {
    if (RX_Frequency_Tens > 6) {
      RX_Frequency_Tens = 6;
    }
  }
  if (RX_Frequency_Units < 4) {
    if (RX_Frequency_Tens < 4) {
      RX_Frequency_Tens = 4;
    }
  }
  
  if ((RX_Frequency_Tenths > 0 || RX_Frequency_Hundredths > 0) & RX_Frequency_Units > 3) {
    if (RX_Frequency_Tens > 6) {
      RX_Frequency_Tens = 6;
    }
  }
}

void switchRX_Frequency_Units() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    RX_Frequency_Units--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    RX_Frequency_Units++;
    delay(200);
  }
  
  if (RX_Frequency_Units < 0) {
    RX_Frequency_Units = 0;
  }
  if (RX_Frequency_Units > 9) {
    RX_Frequency_Units = 9;
  }
  
  switch(RX_Frequency_Tens) {
    case 3:
    if (RX_Frequency_Units < 4) {
      RX_Frequency_Units = 4;
    }
    if (RX_Frequency_Units > 9) {
      RX_Frequency_Units = 9;
    }
    break;
    case 7:
    if (RX_Frequency_Units < 0) {
      RX_Frequency_Units = 0;
    }
    if (RX_Frequency_Units > 4) {
      RX_Frequency_Units = 4;
    }
    break;
  }
  
  if ((RX_Frequency_Tenths > 0 || RX_Frequency_Hundredths > 0) & RX_Frequency_Tens > 6) {
    if (RX_Frequency_Units > 3) {
      RX_Frequency_Units = 3;
    }
  }
}

void switchRX_Frequency_Tenths() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    RX_Frequency_Tenths--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    RX_Frequency_Tenths++;
    delay(200);
  }
  
  if (RX_Frequency_Tenths < 0) {
    RX_Frequency_Tenths = 0;
  }
  if (RX_Frequency_Tenths > 9) {
    RX_Frequency_Tenths = 9;
  }
  
  if (RX_Frequency_Tens == 7 & RX_Frequency_Units == 4) {
    RX_Frequency_Tenths = 0;
  }
}

void switchRX_Frequency_Hundredths() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    RX_Frequency_Hundredths = RX_Frequency_Hundredths - bandwidth[indexBandwidth]*10;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    RX_Frequency_Hundredths = RX_Frequency_Hundredths + bandwidth[indexBandwidth]*10;
    delay(200);
  }
  
  if (RX_Frequency_Hundredths < 0) {
    RX_Frequency_Hundredths = 0;
  }
  if (RX_Frequency_Hundredths > 875) {
    RX_Frequency_Hundredths = 875;
  }
  
  if (RX_Frequency_Tens == 7 & RX_Frequency_Units == 4) {
    RX_Frequency_Hundredths = 0;
  }
}

void switchTX_CTCSS_Tens() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    TX_CTCSS_Tens--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    TX_CTCSS_Tens++;
    delay(200);
  }
  
  if (TX_CTCSS_Tens < 0) {
    TX_CTCSS_Tens = 0; // Minimum
  }
  if (TX_CTCSS_Tens > 3) {
    TX_CTCSS_Tens = 3; // Maximum
  }
  // Case: 00X9. X will be 2. (0029)
  if (TX_CTCSS_Units > 8) {
    if (TX_CTCSS_Tens > 2) {
      TX_CTCSS_Tens = 2;
    }
  }
}

void switchTX_CTCSS_Units() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    TX_CTCSS_Units--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    TX_CTCSS_Units++;
    delay(200);
  }
  // Case: 002X, 0-9
  if (TX_CTCSS_Tens < 3) {
    if (TX_CTCSS_Units < 0) {
      TX_CTCSS_Units = 0;
    }
    if (TX_CTCSS_Units > 9) {
      TX_CTCSS_Units = 9;
    }
  }
  // Case: 003X, 0-8
  else if (TX_CTCSS_Tens = 3) {
    if (TX_CTCSS_Units < 0) {
      TX_CTCSS_Units = 0;
    }
    if (TX_CTCSS_Units > 8) {
      TX_CTCSS_Units = 8;
    }
  }
}

void switchRX_CTCSS_Tens() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    RX_CTCSS_Tens--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    RX_CTCSS_Tens++;
    delay(200);
  }
  
  if (RX_CTCSS_Tens < 0) {
    RX_CTCSS_Tens = 0;
  }
  if (RX_CTCSS_Tens > 3) {
    RX_CTCSS_Tens = 3;
  }
  
  if (RX_CTCSS_Units > 8) {
    if (RX_CTCSS_Tens > 2) {
      RX_CTCSS_Tens = 2;
    }
  }
}

void switchRX_CTCSS_Units() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    RX_CTCSS_Units--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    RX_CTCSS_Units++;
    delay(200);
  }
  
  if (RX_CTCSS_Tens < 3) {
    if (RX_CTCSS_Units < 0) {
      RX_CTCSS_Units = 0;
    }
    if (RX_CTCSS_Units > 9) {
      RX_CTCSS_Units = 9;
    }
  }
  
  else if (RX_CTCSS_Tens = 3) {
    if (RX_CTCSS_Units < 0) {
      TX_CTCSS_Units = 0;
    }
    if (RX_CTCSS_Units > 8) {
      RX_CTCSS_Units = 8;
    }
  }
}

void switchSquelch() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    squelch--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    squelch++;
    delay(200);
  }
  
  if (squelch < 0) {
    squelch = 0; // Minimum
  }
  if (squelch > 8) {
    squelch = 8; // Maximum
  }
}

void switchVolume() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    volume--;
    delay(200);
  }
  if (digitalRead(TACT_SWITCH_NEXT)) {
    volume++;
    delay(200);
  }
  
  if (volume < 1) {
    volume = 1; // Minimum
  }
  if (volume > 8) {
    volume = 8; // Maximum
  }
}

void switchBackHome() {
  
  if (digitalRead(TACT_SWITCH_BACK)) {
    subHome = 1;
    delay(200);
  }
}

void switchBackVHF() {
  
  if (digitalRead(TACT_SWITCH_SELECT)) {
    subVHF = 1;
    delay(200);
  }
}

void switchPTT() {
  
  if (digitalRead(TACT_SWITCH_PTT)) {
    VHF_PTT_State = "TRANSMIT MODE";
    digitalWrite(VHF_PTT,LOW);
  }
  else {
    VHF_PTT_State = "RECEIVE MODE";
    digitalWrite(VHF_PTT,HIGH);
  }
}

void updateHome() {
  
  battery();
  
  switch(menuHome) {
    
    case 0:
    menuHome = 1;
    break;
    
    case 1:
    displayTextSettings();
    
    display.println("HOME");
    display.println("");
    display.println(">Ambience");
    display.println("Compass");
    display.println("GPS Location");
    display.println("VHF Radio");
    
    display.display();
    break;
    
    case 2:
    displayTextSettings();
    
    display.println("HOME");
    display.println("");
    display.println("Ambience");
    display.println(">Compass");
    display.println("GPS Location");
    display.println("VHF Radio");
    
    display.display();
    break;
    
    case 3:
    displayTextSettings();
    
    display.println("HOME");
    display.println("");
    display.println("Ambience");
    display.println("Compass");
    display.println(">GPS Location");
    display.println("VHF Radio");
    
    display.display();
    break;
    
    case 4:
    displayTextSettings();
    
    display.println("HOME");
    display.println("");
    display.println("Ambience");
    display.println("Compass");
    display.println("GPS Location");
    display.println(">VHF Radio");
    
    display.display();
    break;
    
    case 5:
    menuHome = 4;
    break;
  }
}

void updateVHF() {
  
  switch(menuVHF) {
    case 0:
    menuVHF = 1;
    break;
    
    case 1:
    subHome = 1;
    menuVHF = 2;
    break;
    
    case 2:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println(VHF_PTT_State);
    display.println("");
    display.println("Bandwidth");
    display.print(bandwidth[indexBandwidth],4);
    display.println(" kHz");
    
    displayBack();
    display.display();
    break;
    
    case 3:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println(VHF_PTT_State);
    display.println("");
    display.println("Bandwidth");
    display.print(">");
    display.print(bandwidth[indexBandwidth],4);
    display.println(" kHz");
    
    display.display();
    break;
    
    case 4:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println(VHF_PTT_State);
    display.println("");
    display.println("Bandwidth");
    display.print(bandwidth[indexBandwidth],4);
    display.println(" kHz");
    
    displayNext();
    display.display();
    break;
    
    case 5:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    displayBack();
    display.display();
    break;
    
    case 6:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(">");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    display.display();
    break;
    
    case 7:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(">");
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    display.display();
    break;
    
    case 8:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(">");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    display.display();
    break;
    
    case 9:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(">");
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    display.display();
    break;
    
    case 10:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(">");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    display.display();
    break;
    
    case 11:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(">");
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    display.display();
    break;
    
    case 12:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(">");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    display.display();
    break;
    
    case 13:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(">");
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");
    
    display.display();
    break;
    
    case 14:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX Frequency");
    display.print("1");
    display.print(TX_Frequency_Tens);
    display.print(TX_Frequency_Units);
    display.print(".");
    display.print(TX_Frequency_Tenths);
    display.print(TX_Frequency_Hundredths);
    display.println(" MHz");
    display.println("RX Frequency");
    display.print("1");
    display.print(RX_Frequency_Tens);
    display.print(RX_Frequency_Units);
    display.print(".");
    display.print(RX_Frequency_Tenths);
    display.print(RX_Frequency_Hundredths);
    display.println(" MHz");

    displayNext();
    display.display();
    break;
    
    case 15:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX-CTCSS");
    display.print("00");
    display.print(TX_CTCSS_Tens);
    display.println(TX_CTCSS_Units);
    display.println("RX-CTCSS");
    display.print("00");
    display.print(RX_CTCSS_Tens);
    display.println(RX_CTCSS_Units);
    
    displayBack();
    display.display();
    break;
    
    case 16:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX-CTCSS");
    display.print("00");
    display.print(">");
    display.print(TX_CTCSS_Tens);
    display.println(TX_CTCSS_Units);
    display.println("RX-CTCSS");
    display.print("00");
    display.print(RX_CTCSS_Tens);
    display.println(RX_CTCSS_Units);
    
    display.display();
    break;
    
    case 17:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX-CTCSS");
    display.print("00");
    display.print(TX_CTCSS_Tens);
    display.print(">");
    display.println(TX_CTCSS_Units);
    display.println("RX-CTCSS");
    display.print("00");
    display.print(RX_CTCSS_Tens);
    display.println(RX_CTCSS_Units);
    
    display.display();
    break;
    
    case 18:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX-CTCSS");
    display.print("00");
    display.print(TX_CTCSS_Tens);
    display.println(TX_CTCSS_Units);
    display.println("RX-CTCSS");
    display.print("00");
    display.print(">");
    display.print(RX_CTCSS_Tens);
    display.println(RX_CTCSS_Units);
    
    display.display();
    break;
    
    case 19:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX-CTCSS");
    display.print("00");
    display.print(TX_CTCSS_Tens);
    display.println(TX_CTCSS_Units);
    display.println("RX-CTCSS");
    display.print("00");
    display.print(RX_CTCSS_Tens);
    display.print(">");
    display.println(RX_CTCSS_Units);
    
    display.display();
    break;
    
    case 20:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("TX-CTCSS");
    display.print("00");
    display.print(TX_CTCSS_Tens);
    display.println(TX_CTCSS_Units);
    display.println("RX-CTCSS");
    display.print("00");
    display.print(RX_CTCSS_Tens);
    display.println(RX_CTCSS_Units);

    displayNext();
    display.display();
    break;
    
    case 21:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("Squelch");
    display.println(squelch);
    display.println("Volume");
    display.println(volume);
    
    displayBack();
    display.display();
    break;
    
    case 22:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("Squelch");
    display.print(">");
    display.println(squelch);
    display.println("Volume");
    display.println(volume);
    
    display.display();
    break;
    
    case 23:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("Squelch");
    display.println(squelch);
    display.println("Volume");
    display.print(">");
    display.println(volume);
    
    display.display();
    break;
    
    case 24:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("Squelch");
    display.println(squelch);
    display.println("Volume");
    display.println(volume);
    
    displayNext();
    display.display();
    break;
    
    case 25:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println("Scan Frequency");
    
    displayBack();
    display.display();
    break;
    
    case 26:
    displayTextSettings();
    
    display.println("VHF RADIO");
    display.println("");
    display.println(">Scan Frequency");
    
    display.display();
    break;
    
    case 27:
    menuVHF = 26;
    break;
  }
}

void executeHome() {
  
  switch(menuHome) {
    case 1:
    subHome = 2;
    break;
    case 2:
    subHome = 3;
    break;
    case 3:
    subHome = 4;
    break;
    case 4:
    subHome = 5;
    break;
  }
}

void executeVHF() {
  
  switch(menuVHF) {
    case 2:
    subVHF = 1;
    break;
    case 3:
    subVHF = 2;
    break;
    case 6:
    subVHF = 3;
    break;
    case 7:
    subVHF = 4;
    break;
    case 8:
    subVHF = 5;
    break;
    case 9:
    subVHF = 6;
    break;
    case 10:
    subVHF = 7;
    break;
    case 11:
    subVHF = 8;
    break;
    case 12:
    subVHF = 9;
    break;
    case 13:
    subVHF = 10;
    break;
    case 16:
    subVHF = 11;
    break;
    case 17:
    subVHF = 12;
    break;
    case 18:
    subVHF = 13;
    break;
    case 19:
    subVHF = 14;
    break;
    case 22:
    subVHF = 15;
    break;
    case 23:
    subVHF = 16;
    break;
  }
}

void displayTextSettings() {
  
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
}

void displayBack() {
  
  display.setCursor(0,55);
  display.println("<");
}

void displayNext() {
  
  display.setCursor(122,55);
  display.println(">");
}

void displayAmbience() {
  
  displayTextSettings();
  
  display.println("AMBIENCE");
  display.println("");
  display.print("Temperature:");
  display.print(HT.readTemperature());
  display.println(" C");
  display.print("Humidity:");
  display.print(HT.readHumidity());
  display.println(" %");
  
  displayBack();
  display.display();
}

void displayCompass() {
  
  displayTextSettings();
  
  display.println("COMPASS");
  
  displayBack();
  display.display();
}

void displayGPS() {
  
  serialGPS.listen();
  serialGPS.setTimeout(TIMEOUT);
  
  displayTextSettings();
  
  while(serialGPS.available()>0){
    
    GPS.encode(serialGPS.read());
    
    if (GPS.location.isUpdated()){
      display.println("GPS Location");
      display.println("");
      display.println("Latitude:");
      GPS_Latitude = GPS.location.lat(),6;
      display.println(GPS_Latitude);
      display.println("Longitude:");
      GPS_Longitude = GPS.location.lng(),6;
      display.println(GPS_Longitude);
      
      displayBack();
      display.display();
    }
  }
}

void editBandwidth() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println(VHF_PTT_State);
  display.println("");
  display.println("Bandwidth");
  display.println(">");
  display.setCursor(6*8,8*5);
  display.println(" kHz");
  display.display();
  
  display.setCursor(6*1,8*5);
  display.print(bandwidth[indexBandwidth],4);
  blinkText();
}

void editTX_Frequency_Tens() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX Frequency");
  display.print("1");
  display.print(">");
  display.setCursor(6*3,8*3);
  display.print(TX_Frequency_Units);
  display.print(".");
  display.print(TX_Frequency_Tenths);
  display.print(TX_Frequency_Hundredths);
  display.println(" MHz");
  display.println("RX Frequency");
  display.print("1");
  display.print(RX_Frequency_Tens);
  display.print(RX_Frequency_Units);
  display.print(".");
  display.print(RX_Frequency_Tenths);
  display.print(RX_Frequency_Hundredths);
  display.println(" MHz");
  display.display();
  
  display.setCursor(6*2,8*3);
  display.print(TX_Frequency_Tens);
  blinkText();
}

void editTX_Frequency_Units() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX Frequency");
  display.print("1");
  display.print(TX_Frequency_Tens);
  display.print(">");
  display.setCursor(6*4,8*3);
  display.print(".");
  display.print(TX_Frequency_Tenths);
  display.print(TX_Frequency_Hundredths);
  display.println(" MHz");
  display.println("RX Frequency");
  display.print("1");
  display.print(RX_Frequency_Tens);
  display.print(RX_Frequency_Units);
  display.print(".");
  display.print(RX_Frequency_Tenths);
  display.print(RX_Frequency_Hundredths);
  display.println(" MHz");
  display.display();
  
  display.setCursor(6*3,8*3);
  display.print(TX_Frequency_Units);
  blinkText();
}

void editTX_Frequency_Tenths() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX Frequency");
  display.print("1");
  display.print(TX_Frequency_Tens);
  display.print(TX_Frequency_Units);
  display.print(".");
  display.print(">");
  display.setCursor(6*6,8*3);
  display.print(TX_Frequency_Hundredths);
  display.println(" MHz");
  display.println("RX Frequency");
  display.print("1");
  display.print(RX_Frequency_Tens);
  display.print(RX_Frequency_Units);
  display.print(".");
  display.print(RX_Frequency_Tenths);
  display.print(RX_Frequency_Hundredths);
  display.println(" MHz");
  display.display();
  
  display.setCursor(6*5,8*3);
  display.print(TX_Frequency_Tenths);
  blinkText();
}

void editTX_Frequency_Hundredths() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX Frequency");
  display.print("1");
  display.print(TX_Frequency_Tens);
  display.print(TX_Frequency_Units);
  display.print(".");
  display.print(TX_Frequency_Tenths);
  display.print(">");
  display.setCursor(6*9,8*3);
  display.println(" MHz");
  display.println("RX Frequency");
  display.print("1");
  display.print(RX_Frequency_Tens);
  display.print(RX_Frequency_Units);
  display.print(".");
  display.print(RX_Frequency_Tenths);
  display.print(RX_Frequency_Hundredths);
  display.println(" MHz");
  display.display();
  
  display.setCursor(6*6,8*3);
  display.print(TX_Frequency_Hundredths);
  blinkText();
}

void editRX_Frequency_Tens() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX Frequency");
  display.print("1");
  display.print(TX_Frequency_Tens);
  display.print(TX_Frequency_Units);
  display.print(".");
  display.print(TX_Frequency_Tenths);
  display.print(TX_Frequency_Hundredths);
  display.println(" MHz");
  display.println("RX Frequency");
  display.print("1");
  display.print(">");
  display.setCursor(6*3,8*5);
  display.print(RX_Frequency_Units);
  display.print(".");
  display.print(RX_Frequency_Tenths);
  display.print(RX_Frequency_Hundredths);
  display.println(" MHz");
  display.display();
  
  display.setCursor(6*2,8*5);
  display.print(RX_Frequency_Tens);
  blinkText();
}

void editRX_Frequency_Units() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX Frequency");
  display.print("1");
  display.print(TX_Frequency_Tens);
  display.print(TX_Frequency_Units);
  display.print(".");
  display.print(TX_Frequency_Tenths);
  display.print(TX_Frequency_Hundredths);
  display.println(" MHz");
  display.println("RX Frequency");
  display.print("1");
  display.print(RX_Frequency_Tens);
  display.print(">");
  display.setCursor(6*4,8*5);
  display.print(".");
  display.print(RX_Frequency_Tenths);
  display.print(RX_Frequency_Hundredths);
  display.println(" MHz");
  display.display();
  
  display.setCursor(6*3,8*5);
  display.print(RX_Frequency_Units);
  blinkText();
}

void editRX_Frequency_Tenths() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX Frequency");
  display.print("1");
  display.print(TX_Frequency_Tens);
  display.print(TX_Frequency_Units);
  display.print(".");
  display.print(TX_Frequency_Tenths);
  display.print(TX_Frequency_Hundredths);
  display.println(" MHz");
  display.println("RX Frequency");
  display.print("1");
  display.print(RX_Frequency_Tens);
  display.print(RX_Frequency_Units);
  display.print(".");
  display.print(">");
  display.setCursor(6*6,8*5);
  display.print(RX_Frequency_Hundredths);
  display.println(" MHz");
  display.display();
  
  display.setCursor(6*5,8*5);
  display.print(RX_Frequency_Tenths);
  blinkText();
}

void editRX_Frequency_Hundredths() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX Frequency");
  display.print("1");
  display.print(TX_Frequency_Tens);
  display.print(TX_Frequency_Units);
  display.print(".");
  display.print(TX_Frequency_Tenths);
  display.print(TX_Frequency_Hundredths);
  display.println(" MHz");
  display.println("RX Frequency");
  display.print("1");
  display.print(RX_Frequency_Tens);
  display.print(RX_Frequency_Units);
  display.print(".");
  display.print(RX_Frequency_Tenths);
  display.print(">");
  display.setCursor(6*9,8*5);
  display.println(" MHz");
  display.display();
  
  display.setCursor(6*6,8*5);
  display.print(RX_Frequency_Hundredths);
  blinkText();
}

void editTX_CTCSS_Tens() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX-CTCSS");
  display.print("00");
  display.print(">");
  display.setCursor(6*4,8*3);
  display.println(TX_CTCSS_Units);
  display.println("RX-CTCSS");
  display.print("00");
  display.print(RX_CTCSS_Tens);
  display.println(RX_CTCSS_Units);
  display.display();
  
  display.setCursor(6*3,8*3);
  display.print(TX_CTCSS_Tens);
  blinkText();
}

void editTX_CTCSS_Units() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX-CTCSS");
  display.print("00");
  display.print(TX_CTCSS_Tens);
  display.print(">");
  display.setCursor(0,8*4);
  display.println("RX-CTCSS");
  display.print("00");
  display.print(RX_CTCSS_Tens);
  display.println(RX_CTCSS_Units);
  display.display();
  
  display.setCursor(6*4,8*3);
  display.print(TX_CTCSS_Units);
  blinkText();
}

void editRX_CTCSS_Tens() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX-CTCSS");
  display.print("00");
  display.print(TX_CTCSS_Tens);
  display.println(TX_CTCSS_Units);
  display.println("RX-CTCSS");
  display.print("00");
  display.print(">");
  display.setCursor(6*4,8*5);
  display.println(RX_CTCSS_Units);
  display.display();
  
  display.setCursor(6*3,8*5);
  display.print(RX_CTCSS_Tens);
  blinkText();
}

void editRX_CTCSS_Units() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("TX-CTCSS");
  display.print("00");
  display.print(TX_CTCSS_Tens);
  display.println(TX_CTCSS_Units);
  display.println("RX-CTCSS");
  display.print("00");
  display.print(RX_CTCSS_Tens);
  display.print(">");
  display.display();
  
  display.setCursor(6*4,8*5);
  display.print(RX_CTCSS_Units);
  blinkText();
}

void editSquelch() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("Squelch");
  display.println(">");
  display.println("Volume");
  display.println(volume);
  display.display();
  
  display.setCursor(6*1,8*3);
  display.println(squelch);
  blinkText();
}

void editVolume() {
  
  displayTextSettings();
  
  display.println("VHF RADIO");
  display.println("");
  display.println("Squelch");
  display.println(squelch);
  display.println("Volume");
  display.println(">");
  display.display();
  
  display.setCursor(6*1,8*5);
  display.println(volume);
  blinkText();
}

void handshakeVHF() {
  
  serialVHF.listen();
  serialVHF.setTimeout(TIMEOUT);
  
  serialVHF.println("AT+DMOCONNECT");
}

void setGroupVHF() {
  
  serialVHF.listen();
  serialVHF.setTimeout(TIMEOUT);
  
  serialVHF.print("AT+DMOSETGROUP=");
  serialVHF.print(indexBandwidth);
  serialVHF.print(",1");
  serialVHF.print(TX_Frequency_Tens);
  serialVHF.print(TX_Frequency_Units);
  serialVHF.print(".");
  serialVHF.print(TX_Frequency_Tenths);
  
  if (TX_Frequency_Hundredths == 0) {
    serialVHF.print("000");
  }
  if (TX_Frequency_Hundredths > 0) {
    serialVHF.print(TX_Frequency_Hundredths);
  }
  
  serialVHF.print(",1");
  serialVHF.print(RX_Frequency_Tens);
  serialVHF.print(RX_Frequency_Units);
  serialVHF.print(".");
  serialVHF.print(RX_Frequency_Tenths);
  
  if (RX_Frequency_Hundredths == 0) {
    serialVHF.print("000");
  }
  if (RX_Frequency_Hundredths > 0) {
    serialVHF.print(RX_Frequency_Hundredths);
  }
  
  serialVHF.print(",00");
  serialVHF.print(TX_CTCSS_Tens);
  serialVHF.print(TX_CTCSS_Units);
  serialVHF.print(",");
  serialVHF.print(squelch);
  serialVHF.print(",00");
  serialVHF.print(RX_CTCSS_Tens);
  serialVHF.println(RX_CTCSS_Units);
}

void setVolumeVHF() {
  
  serialVHF.listen();
  serialVHF.setTimeout(TIMEOUT);
  
  serialVHF.print("AT+DMOSETVOLUME=");
  serialVHF.println(volume);
}

void sendMessageGSM() {
  
  serialGSM.listen();
  serialGSM.setTimeout(TIMEOUT);
  
  serialGSM.println("AT+CMGF=1");
  delay(200);
  serialGSM.println("AT+CMGS=\"" + GSM_Number + "\"\r");
  delay(200);
  serialGSM.println("Latitude:");
  serialGSM.println(GPS_Latitude);
  serialGSM.println("Longitude:");
  serialGSM.println(GPS_Longitude);
  serialGSM.println((char)26);
}
