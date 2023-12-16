#include <RTClib.h> // for the RTC

RTC_DS1307 rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
void setup () {
  while (!Serial); // for Leonardo/Micro/Zero
  Serial.begin(57600);
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  } else {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  if (! rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    // following line sets the RTC to the date & time this sketch was compiled
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }
}
void printClock() {
  DateTime now = rtc.now();
  Serial.print("Date ");
  if (now.month() < 10) {         // Zero padding if value less than 10 ie."09" instead of "9"
    Serial.print("0");
    Serial.print(now.month(), DEC);
  } else {
    Serial.print(now.month(), DEC);
  }
  Serial.print('/');
  if (now.day() < 10) {          // Zero padding if value less than 10 ie."09" instead of "9"
    Serial.print("0");
    Serial.print(now.day(), DEC);
  } else {
    Serial.print(now.day(), DEC);
  }
  Serial.print('/');
  Serial.println(now.year(), DEC);
  /*************  Now comes the time section  **************/
  const uint8_t h = now.hour();
  const uint8_t hr_12 = h % 12;
  Serial.print("Time ");
  if (hr_12 < 10) {              // Zero padding if value less than 10 ie."09" instead of "9"
    Serial.print(" ");
    Serial.print((h > 12) ? h - 12 : ((h == 0) ? 12 : h), DEC); // Conversion to AM/PM
  }
  else {
    Serial.print((h > 12) ? h - 12 : ((h == 0) ? 12 : h), DEC); // Conversion to AM/PM
  }
  Serial.print(':');
  if (now.minute() < 10) {       // Zero padding if value less than 10 ie."09" instead of "9"
    Serial.print("0");
    Serial.print(now.minute(), DEC);
  }
  else {
    Serial.print(now.minute(), DEC);
  }
  Serial.print(':');
  if (now.second() < 10) {      // Zero padding if value less than 10 ie."09" instead of "9"
    Serial.print("0");
    Serial.print(now.second(), DEC);
  }
  else {
    Serial.print(now.second(), DEC);
  }
  if (h < 12) {                // Adding the AM/PM sufffix
    Serial.println(" AM");
  }
  else {
    Serial.println(" PM");
  }
}
void loop () {
  /*
    DateTime now = rtc.now();
    Serial.print(now.year(), DEC);
    Serial.print('/');
    Serial.print(now.month(), DEC);
    Serial.print('/');
    Serial.print(now.day(), DEC);
    Serial.print(" (");
    Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
    Serial.print(") ");
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
  */
  printClock();
  delay(1000);
}
