#include <SPI.h>
#include <RH_RF69.h>
#include <RHReliableDatagram.h>

#include <Wire.h>
#include <U8glib.h>

#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>

#define DEBOUNCE_TIME 250

#define SERIAL_GPS_RX 9
#define SERIAL_GPS_TX 10
#define GPS_BAUD 9600

// Change to 434.0 or other frequency, must match RX's freq!
#define RF69_FREQ 434.0
// Where to send packets to!
#define DEST_ADDRESS   255
// change addresses for each client board, any number :)
#define MY_ADDRESS     20
// Pinouts
#define RFM69_CS      A3
#define RFM69_RST     A2
#define RFM69_IRQ     2

// Singleton instance of the radio driver
RH_RF69 rf69(RFM69_CS, RFM69_IRQ);

// Class to manage message delivery and receipt, using the driver declared above
RHReliableDatagram rf69_manager(rf69, MY_ADDRESS);

U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_DEV_0 | U8G_I2C_OPT_FAST);

SoftwareSerial serial_GPS(SERIAL_GPS_RX, SERIAL_GPS_TX);
TinyGPSPlus gps;

//////////////// DHT ////////////////////
#include <DHT.h>
#define DHTPIN A0
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
// DHT Calibration
float humidity_scale = 0.9375; // SLOPE
float humidity_offset = 2.3125; // OFFSET
/////////////////////////////////////////

char chars[37] = {'a', 'b', 'c', 'd', 'e',
                  'f', 'g', 'h', 'i', 'j',
                  'k', 'l', 'm', 'n', 'o',
                  'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z',
                  '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' '
                 };

uint8_t char_counter = 0;
String will_send_msg = "";
String last_received_from = "ADDR";
String last_received_msg_prev = "";
String last_received_msg = "";
String last_RSSI = "RSSI";

bool is_gps = false;

int get_dht_temp() {
  int t = dht.readTemperature();
  if (isnan(t))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  return t;
}

int get_dht_humid() {
  int h = dht.readHumidity();
  if (isnan(h))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  return (h * humidity_scale + humidity_offset);
}

void do_receive(int packetsize) {
  uint8_t buf[packetsize];
  if (rf69_manager.available())
  {
    // Wait for a message addressed to us from the client
    uint8_t len = sizeof(buf);
    uint8_t from;
    if (rf69_manager.recvfromAck(buf, &len, &from)) {
      buf[len] = 0; // zero out remaining string
      Serial.println("Got packet from #" + String(from));
      Serial.println("RSSI: " + String(rf69.lastRssi()));
      Serial.println("Message: " + String((char*)buf));

      // if message is for this device, or broadcast, print details:
      last_received_from = String(from);
      last_received_msg_prev = last_received_msg;
      last_received_msg = String((char*)buf);
      last_RSSI = String(rf69.lastRssi());
    }
  }
}

void do_transmit(String message, int packetsize) {
  // convert string to char array
  char radiopacket[packetsize];
  message.toCharArray(radiopacket, packetsize);
  Serial.println("Sending: " + String(radiopacket));
  // Send a message to the DESTINATION!
  if (rf69_manager.sendtoWait((uint8_t *)radiopacket, strlen(radiopacket), DEST_ADDRESS)) {
    Serial.println(F("Sent"));
  }
}

void reset_message()
{
  is_gps = false;
  will_send_msg = "";
}

void accept_char()
{
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  if (interrupt_time - last_interrupt_time > DEBOUNCE_TIME)
  {
    will_send_msg += chars[char_counter];
  }
  last_interrupt_time = interrupt_time;
}

void backward_char()
{
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  if (interrupt_time - last_interrupt_time > DEBOUNCE_TIME)
  {
    if (char_counter > 0)
    {
      char_counter -= 1;
    }
    else
      char_counter = sizeof(chars) / sizeof(chars[0]) - 1;
    last_interrupt_time = interrupt_time;
  }
}

void forward_char()
{
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  if (interrupt_time - last_interrupt_time > DEBOUNCE_TIME)
  {
    if (char_counter < sizeof(chars) / sizeof(chars[0]) - 1)
    {
      char_counter += 1;
    }
    else
      char_counter = 0;
    last_interrupt_time = interrupt_time;
  }
}

void send_message()
{
  if (will_send_msg != "")
  {
    if (is_gps) {
      will_send_msg = will_send_msg;
      is_gps = false;
    } else
    {
      will_send_msg = String(get_dht_temp()) + "," + String(get_dht_humid()) + "," + will_send_msg;
    }
    do_transmit(will_send_msg, 30);
    will_send_msg = ""; // reset message
  }
}

void get_gps()
{
  while (serial_GPS.available() > 0)
  {
    if (gps.encode(serial_GPS.read()))
    {
      if (gps.location.isValid())
      {
        is_gps = true;
        will_send_msg = String(gps.location.lat(), 6) + "N" +
                        String(gps.location.lng(), 6) + "E";
        show_display();
      }
      else
      {
        Serial.println(F("INVALID"));
      }
    }
  }
}

void show_display()
{
  u8g.firstPage();
  do
  {
    u8g.setFont(u8g_font_helvR08);

    u8g.setPrintPos(0, 10);
    u8g.print(F("Char: "));
    u8g.print(chars[char_counter]);

    u8g.setPrintPos(100, 10);
    u8g.print(String(MY_ADDRESS));

    u8g.setPrintPos(0, 20);
    u8g.print(F("Send ("));
    u8g.print(String(DEST_ADDRESS));
    u8g.print(F("):"));

    u8g.setPrintPos(0, 30);
    u8g.print(will_send_msg);

    u8g.setPrintPos(0, 40);
    u8g.print(F("Last ("));
    u8g.print(last_received_from);
    u8g.print(F(","));
    u8g.print(last_RSSI);
    u8g.print(F("):"));

    u8g.setPrintPos(0, 50);
    u8g.print(last_received_msg);

    u8g.setPrintPos(0, 60);
    u8g.print(last_received_msg_prev);
  } while (u8g.nextPage());
  u8g.nextPage();
}

void setup()
{
  // Serial Monitor
  Serial.begin(9600);

  // GPS
  serial_GPS.begin(GPS_BAUD);

  // Pinmode
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(3), accept_char, RISING);


  // RF69 ////////////////////////////////////////////////////////////////////////////////////////////////

  // set reset
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, LOW);

  // manual reset
  digitalWrite(RFM69_RST, HIGH);
  delay(10);
  digitalWrite(RFM69_RST, LOW);
  delay(10);

  // init RF69
  if (!rf69_manager.init()) {
    Serial.println(F("RFM69 radio init failed"));
    while (1);
  } else Serial.println(F("RFM69 radio init OK!"));

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM (for low power module)
  if (!rf69.setFrequency(RF69_FREQ)) {
    Serial.println(F("setFrequency failed"));
  }

  // If you are using a high power RF69 eg RFM69HW, you *must* set a Tx power with the
  // ishighpowermodule flag set like this:
  rf69.setTxPower(20, true);  // range from 14-20 for power, 2nd arg must be true for 69HCW

  // print details
  Serial.println("RFM69 radio @" + String((int)RF69_FREQ) + String(" MHz"));

  /////////////////////////////////////////////////////////////////////////////////////////////////////////

  // DHT Begin
  dht.begin();
}

void loop()
{
  if (digitalRead(4) == LOW)
  {
    backward_char();
  }
  else if (digitalRead(5) == LOW)
  {
    reset_message();
  }
  else if (digitalRead(6) == LOW)
  {
    get_gps();
  }
  else if (digitalRead(7) == LOW)
  {
    send_message();
  }
  else if (digitalRead(8) == LOW)
  {
    forward_char();
  }

  if (digitalRead(6) != LOW)
  {
    show_display();
  }

  do_receive(30);
}
