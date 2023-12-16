#include <SPI.h>
#include <LoRa.h>

#include <Wire.h>
#include <U8glib.h>

#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>

#define DEBOUNCE_TIME 250

#define SERIAL_GPS_RX 9
#define SERIAL_GPS_TX 10
#define GPS_BAUD 9600

#define LORA_CS_PIN A3
#define LORA_RST_PIN A2
#define LORA_IRQ_PIN 2

#define SPREADING_FACTOR 12
#define SYNC_WORD 0x35
#define CODING_RATE_4 8

#define LOCAL_ADDRESS 0xBB
#define DESTINATION_ADDRESS 0xFF
#define RADIO_FREQUENCY 433E6

U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_DEV_0 | U8G_I2C_OPT_FAST);

SoftwareSerial serial_GPS(SERIAL_GPS_RX, SERIAL_GPS_TX);
TinyGPSPlus gps;

char chars[37] = {'a', 'b', 'c', 'd', 'e',
                  'f', 'g', 'h', 'i', 'j',
                  'k', 'l', 'm', 'n', 'o',
                  'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z',
                  '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' '};

uint8_t char_counter = 0;
String will_send_msg = "";
String last_received_from = "ADDR";
String last_received_msg_prev = "";
String last_received_msg = "";
String last_RSSI = "RSSI";
String last_SNR = "SNR";

void lora_on_receive(int packetSize)
{
  if (packetSize == 0)
    return; // if there's no packet, return

  // read packet header bytes:
  int recipient = LoRa.read();       // recipient address
  byte sender = LoRa.read();         // sender address
  byte incomingMsgId = LoRa.read();  // incoming msg ID
  byte incomingLength = LoRa.read(); // incoming msg length

  String incoming = ""; // payload of packet

  while (LoRa.available())
  {                                // can't use readString() in callback, so
    incoming += (char)LoRa.read(); // add bytes one by one
  }

  if (incomingLength != incoming.length()) // check length for error
  {
    Serial.println("error: message length does not match length");
    return; // skip rest of function
  }

  // if the recipient isn't this device or broadcast,
  if (recipient != LOCAL_ADDRESS && recipient != 0xFF)
  {
    Serial.println("This message is not for me.");
    return; // skip rest of function
  }

  // if message is for this device, or broadcast, print details:
  last_received_from = "0x" + String(sender, HEX);
  last_received_msg_prev = last_received_msg;
  last_received_msg = incoming;
  last_RSSI = String(LoRa.packetRssi());
  last_SNR = String(LoRa.packetSnr());

  Serial.println("Received from: 0x" + last_received_from);
  Serial.println("Sent to: 0x" + String(recipient, HEX));
  Serial.println("Message ID: " + String(incomingMsgId));
  Serial.println("Message length: " + String(incomingLength));
  Serial.println("Message: " + incoming);
  Serial.println("RSSI: " + last_RSSI);
  Serial.println("Snr: " + last_SNR);
  Serial.println();
}

void lora_send_message(String outgoing)
{
  static int msgCount = 0;
  LoRa.beginPacket();              // start packet
  LoRa.write(DESTINATION_ADDRESS); // add destination address
  LoRa.write(LOCAL_ADDRESS);       // add sender address
  LoRa.write(msgCount);            // add message ID
  LoRa.write(outgoing.length());   // add payload length
  LoRa.print(outgoing);            // add payload
  LoRa.endPacket(true);            // finish packet and send it
  msgCount++;                      // increment message ID
}

void reset_message()
{
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
    lora_send_message(will_send_msg);
    LoRa.receive();     // go back into receive mode
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
    u8g.print(F("0x"));
    u8g.print(String(LOCAL_ADDRESS, HEX));

    u8g.setPrintPos(0, 20);
    u8g.print(F("Send (0x"));
    u8g.print(String(DESTINATION_ADDRESS, HEX));
    u8g.print(F("):"));

    u8g.setPrintPos(0, 30);
    u8g.print(will_send_msg);

    u8g.setPrintPos(0, 40);
    u8g.print(F("Last ("));
    u8g.print(last_received_from);
    u8g.print(F(","));
    u8g.print(last_RSSI);
    u8g.print(F(","));
    u8g.print(last_SNR);
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

  // LORAWAN
  LoRa.setPins(LORA_CS_PIN, LORA_RST_PIN, LORA_IRQ_PIN); // set CS, reset, IRQ pin
  LoRa.setSpreadingFactor(SPREADING_FACTOR);
  LoRa.setSyncWord(SYNC_WORD);
  LoRa.setCodingRate4(CODING_RATE_4);

  if (!LoRa.begin(RADIO_FREQUENCY)) // initialize radio at 433 MHz
  {
    Serial.println("LoRa init failed. Check your connections.");
    while (true)
      ; // if failed, do nothing
  }

  LoRa.onReceive(lora_on_receive); // callback
  LoRa.receive();
  Serial.println("LoRa init succeeded.");
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
}
