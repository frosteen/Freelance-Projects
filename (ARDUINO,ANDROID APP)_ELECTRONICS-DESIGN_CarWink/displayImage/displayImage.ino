#include <SPI.h>
#include <SdFat.h>
#include <UTFT.h>
#include <UTFT_SdRaw.h>

#define SD_CHIP_SELECT  53  // SD chip select pin(Arduino Mega)
SdFat sd;

UTFT myGLCD(ILI9341_16, 38, 39, 40, 41);
UTFT_SdRaw myFiles(&myGLCD);

char alphabet[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v'};

void setup()
{
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(115200);
  Serial1.begin(115200);
  delay(100);
  bool mysd = 0;
  while (!mysd)
  {
    if (!sd.begin(SD_CHIP_SELECT, SPI_FULL_SPEED))
    {
      Serial.println(F("Card failed, or not present"));
      Serial.println(F("Retrying...."));
    }
    else
    {
      mysd = 1;
      Serial.println(F("Card initialised."));
    }
  }
  Serial.println(F("Initialising LCD."));
  myGLCD.InitLCD();
  myGLCD.clrScr();
  myFiles.load(0, 0, 320, 240, "theme.raw", 1, 0);
  delay(1000);
  myGLCD.clrScr();
  digitalWrite(13, HIGH);
}

void loop()
{
  while (Serial1.available()) {
    char c = Serial1.read();
    for (int i = 1; i <= 22; i++) {
      char buf = alphabet[i];
      String text = "";
      text += buf;
      text += ".raw";
      const int len = text.length()+1;
      char buf1[len];
      text.toCharArray(buf1,len);
      if (c == buf) {
        myFiles.load(0, 0, 320, 240, buf1, 1, 0);
        break;
      }
    }
  }
}
