const uint8_t PIR_Pins[] = {12, 8, 7, 4}; // Initiate PINS to be used for PIR
const uint8_t BUZZER_Pin = A0; // Initiate PIN to be used for Buzzer
const uint16_t buzzer_frequency = 29000; // Set the frequency to 29KHZ
const uint16_t buzzer_duration = 5000; // On state duration of buzzer (5 SECONDS)

void setup() {
  for (int i = 0; i < sizeof(PIR_Pins) / sizeof(PIR_Pins[0]); i++) {
    pinMode(PIR_Pins[i], INPUT); // Set all the PIR Pins as INPUT
  }
}

void loop() {
  for (int i = 0; i < sizeof(PIR_Pins) / sizeof(PIR_Pins[0]); i++) {
    uint8_t PIR_Pin_val = digitalRead(PIR_Pins[i]); // Read the state (LOW/HIGH) of the PIR Pins
    if (PIR_Pin_val == HIGH) { // Check if HIGH
      tone(BUZZER_Pin, buzzer_frequency); // Set the buzzer frequency then produce the tone
      delay(buzzer_duration); // the duration of buzzer before it turns off
    } else {
      noTone(BUZZER_Pin); // if LOW then there will no tone produced
    }
  }
  delay(100); // Check the state of PIR every 100ms
}
