#include <DHT.h>
#include <IRremote.h>

uint16_t Temp18[109] = {650,3400, 600,500, 600,500, 600,500, 600,450, 650,450, 650,450, 650,1450, 600,1500, 600,500, 600,500, 600,500, 600,500, 600,450, 650,450, 600,500, 600,500, 600,500, 600,450, 650,450, 650,450, 650,450, 600,500, 600,500, 600,500, 600,450, 650,450, 650,450, 600,500, 600,500, 600,500, 650,450, 600,500, 600,500, 600,450, 650,450, 650,450, 600,500, 600,500, 600,1500, 600,500, 600,450, 650,450, 650,450, 650,450, 600,500, 600,500, 600,1450, 650,450, 650,1450, 650,450, 600,500, 600,500, 600,3400, 650};  // Protocol=UNKNOWN Data=0x78132C2E

//uint16_t Temp27[109] = {600,3450, 600,450, 600,450, 650,500, 650,450, 600,450, 650,500, 600,1500, 550,1500, 600,500, 600,450, 650,500, 600,500, 600,450, 650,450, 600,450, 700,450, 600,500, 600,500, 600,400, 650,550, 550,550, 550,500, 600,500, 600,500, 600,450, 650,500, 600,500, 550,500, 600,500, 600,500, 600,500, 600,500, 600,500, 600,450, 650,450, 650,450, 650,400, 650,500, 600,1500, 600,500, 550,550, 550,500, 600,500, 600,500, 600,1500, 600,500, 600,1500, 550,1500, 600,1500, 600,1500, 600,1500, 550,1500, 600,3450, 550};  // Protocol=UNKNOWN Data=0x8D0D7D20

uint16_t Temp30[109] = {600,3450, 600,500, 750,350, 600,450, 650,400, 650,500, 600,500, 600,1500, 600,1500, 550,550, 550,550, 550,500, 600,500, 600,500, 600,500, 600,500, 600,450, 600,500, 600,500, 600,500, 600,500, 600,500, 600,500, 600,500, 600,450, 600,500, 600,500, 650,450, 600,500, 600,450, 650,500, 550,550, 550,550, 550,550, 550,500, 600,500, 600,500, 650,450, 550,550, 550,1500, 600,500, 600,500, 600,500, 600,450, 650,500, 600,1500, 550,1500, 600,1500, 600,500, 600,1500, 550,1550, 550,500, 600,500, 600,3450, 550};  // Protocol=UNKNOWN Data=0x3A80C424

int Desired_temperature = 27;

int Measured_temp;
int Measured_Humi;
int AC_Temp;
char temp_error = 2;
int Pev_value;
int khz = 38; // 38kHz carrier frequency for the NEC protocol

int DHTPIN = 4;

DHT dht(DHTPIN, DHT22);

IRsend irsend;

void setup()
{
  Serial.begin(115200);
  dht.begin();
}

void loop()
{
  //Read data and store it to variables hum and temp
  Measured_Humi = dht.readHumidity() + temp_error;
  Measured_temp= dht.readTemperature();
  //Print temp and humidity values to serial monitor
  Serial.print("Temperature: "); Serial.print(Measured_temp);Serial.println("C");
  Serial.print("Humidity: "); Serial.print(Measured_Humi);Serial.println("%");
  Serial.print("AC Temp: "); Serial.print(AC_Temp);Serial.println("C");

if ( Measured_temp != Pev_value) //Change the temperature only if the measured voltage value changes
{
  if (Measured_temp == Desired_temperature+2) //If AC is ON and measured temp is very very high than desired
  {
    irsend.sendRaw(Temp18, sizeof(Temp18) / sizeof(Temp18[0]), khz); delay(2000);//Send signal to set 24*C
    AC_Temp = 18; 
  }
  
  if (Measured_temp == Desired_temperature ) //If AC is ON and measured temp is desired value
  {
    //irsend.sendRaw(Temp27, sizeof(Temp27) / sizeof(Temp27[0]), khz); //Send signal to set 27*C
    AC_Temp = Desired_temperature; 
  }
  
  
  if (Measured_temp == Desired_temperature-2 ) //If AC is ON and measured temp is very very low desired value
  {
    irsend.sendRaw(Temp30, sizeof(Temp30) / sizeof(Temp30[0]), khz); delay(2000);//Send signal to set 30*C
    AC_Temp = 30; 
  }
  
}
  Pev_value = Measured_temp;
  delay(500);
}
