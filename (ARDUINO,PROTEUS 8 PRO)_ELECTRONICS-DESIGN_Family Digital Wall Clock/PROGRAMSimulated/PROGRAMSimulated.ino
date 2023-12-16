#include<dht.h>
#include <RTClib.h>
#include <LiquidCrystal.h>

int maxSongs = 0;

//MODES
int mode = 0;
int maxMode = 5;
int modePin = 9;
int buttonState = 0;
int buttonState2 = 0;

//ALARM
bool isAlarm = true;
int alarmPin = 10;

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

RTC_DS1307 rtc;
dht DHT;
//DaysOfTheWeek
char daysOfTheWeek[7][4] = {"SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"};

void setup() {
  Serial.begin(9600);
  pinMode(modePin, INPUT);
  pinMode(alarmPin, INPUT);
  pinMode(6, OUTPUT);
  Serial.begin(9600);
  Serial.println(maxSongs);
  lcd.begin(16, 2);
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (true);
  }
  else {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    //RTC.adjust(DateTime(y, mon, d, h, minu, s));
  }
  if (!rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
  }
}

void printModes() {
  DateTime now = rtc.now();
  if (mode == 0) {
    char sentence[8];
    const uint8_t h = now.hour();
    const uint8_t hr_12 = h % 12;
    //AM/PM Time format
    if (h < 12) {
      sprintf(sentence, "%02d:%02dAM", hr_12, now.minute());
      lcd.clear();
      lcd.print(sentence);
      delay(500);
    }
    else {
      sprintf(sentence, "%02d:%02dPM", hr_12, now.minute());
      lcd.clear();
      lcd.print(sentence);
      delay(500);
    }
    //ALARM
    if (h == 3 && now.minute() == 0) {
      Serial.println("Hello World");
      digitalWrite(6, HIGH);
      delay(15000);
      digitalWrite(6, LOW);
      delay(15000);
    }
    else if (h == 14 && now.minute() == 0) {
      digitalWrite(6, HIGH);
      delay(15000);
      digitalWrite(6, LOW);
      delay(15000);
    }
    else if (h == 15 && now.minute() == 0) {
      digitalWrite(6, HIGH);
      delay(15000);
      digitalWrite(6, LOW);
      delay(15000);
    }
    else if (h == 17 && now.minute() == 0) {
      digitalWrite(6, HIGH);
      delay(15000);
      digitalWrite(6, LOW);
      delay(15000);
    }
    else if (h == 20 && now.minute() == 0) {
      digitalWrite(6, HIGH);
      delay(15000);
      digitalWrite(6, LOW);
      delay(15000);
    }
    else if (h == 21 && now.minute() == 0) {
      digitalWrite(6, HIGH);
      delay(15000);
      digitalWrite(6, LOW);
      delay(15000);
    }
  }
  //Days of the Week
  else if (mode == 1) {
    lcd.clear();
    lcd.print(daysOfTheWeek[now.dayOfTheWeek()]);
    delay(500);
  }
  //month.date.year (mm.dd.yy)
  else if (mode == 2) {
    char sentence[8];
    sprintf(sentence, "%02d.%02d.%d", now.month(), now.day(), now.year() % 100);
    lcd.clear();
    lcd.print(sentence);
    delay(500);
  }
  //Temperature
  else if (mode == 3) {
    char sentence[8];
    char str_temp[4];
    DHT.read11(7);
    dtostrf(DHT.temperature, 2, 0, str_temp);
    sprintf(sentence, "T:%sC", str_temp);
    lcd.clear();
    lcd.print(sentence);
    delay(1000);
  }
  //Humidity
  else if (mode == 4) {
    char sentence[8];
    char str_temp[4];
    DHT.read11(7);
    dtostrf(DHT.humidity, 2, 0, str_temp);
    sprintf(sentence, "H:%s%%", str_temp);
    lcd.clear();
    lcd.print(sentence);
    delay(1000);
  }
}

void changeMode() {
  mode += 1;
  if (mode == maxMode) {
    mode = 0;
  }
}

void loop() {
  printModes();
  if (digitalRead(modePin) == HIGH && buttonState == LOW) {
    changeMode();
    buttonState = HIGH;
  }
  else if (digitalRead(modePin) == LOW && buttonState == HIGH) {
    buttonState = LOW;
  }
  if (digitalRead(alarmPin) == HIGH && buttonState2 == LOW) {
    if (isAlarm) {
      isAlarm = false;
      lcd.clear();
      lcd.print("A-OFF");
      delay(2000);
    }
    else {
      isAlarm = true;
      lcd.clear();
      lcd.print("A-ON");
      delay(2000);
    }
    buttonState2 = HIGH;
  }
  else if (digitalRead(alarmPin) == LOW && buttonState2 == HIGH) {
    buttonState2 = LOW;
  }
}
