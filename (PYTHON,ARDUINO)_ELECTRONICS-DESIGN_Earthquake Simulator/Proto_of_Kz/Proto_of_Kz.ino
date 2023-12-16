#include <Servo.h>
#include <Wire.h>              // Library for I2C communication
#include <LiquidCrystal_I2C.h> // Library for LCD

// ADXL345 Libraries
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 20, 4); // Change to (0x27,20,4) for 20x4 LCD.
Servo myservo;
Servo myservo2;      // create servo object to control a servo
#define servoPin 12  //~
#define servoPin2 11 //~
#define pushButtonPin1 8
#define pushButtonPin2 9
#define pushButtonPin3 10

// ADXL345 Object
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

// ADXL345 View Sensor Details
void displaySensorDetails(void) {
  sensor_t sensor;
  accel.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" m/s^2");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" m/s^2");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" m/s^2");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(100);
}

int angle = 95; // initial angle  for servo (beteen 1 and 179)
int angle2 = 95;

int buttonPushed1 = 0;
int buttonPushed2 = 0;
int buttonPushed3 = 0;

char val = '0';

void welcome_message() {
  // Print 'Hello World!' on the first line of the LCD:
  lcd.clear();
  lcd.setCursor(0, 0); // Set the cursor on the third column and first row.
  lcd.print("Welcome to our");
  lcd.setCursor(0, 1);
  lcd.print("Earthquake Simulator");
  lcd.setCursor(0, 2); // Set the cursor on the third column and first row.
  lcd.print("Yellow Start");
  lcd.setCursor(0, 3); // Set the cursor on the third column and first row.
  lcd.print("Blue Stop");
}

void setup() {
  // Servo button demo by Robojax.com
  Serial.begin(9600);       //  setup serial
  myservo.attach(servoPin); // attaches the servo on pin 3 to the servo object
  myservo2.attach(servoPin2);
  pinMode(pushButtonPin1, INPUT_PULLUP);
  pinMode(pushButtonPin2, INPUT_PULLUP);
  pinMode(pushButtonPin3, INPUT_PULLUP);
  Serial.println("Robojax Servo Button ");
  myservo.write(angle);   // initial position
  myservo2.write(angle2); // initial position

  // Initiate ADXL345
  if (!accel.begin()) {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while (1);
  }
  /* Set the range to whatever is appropriate for your project */
  accel.setRange(ADXL345_RANGE_16_G);
  // accel.setRange(ADXL345_RANGE_8_G);
  // accel.setRange(ADXL345_RANGE_4_G);
  // accel.setRange(ADXL345_RANGE_2_G);
  /* Display some basic information on this sensor */
  displaySensorDetails();

  // Initiate the LCD:
  lcd.init();
  lcd.backlight();
  welcome_message();

  Serial.println("Initiate Simulator.");
}

void show_values() {
  /* Get a new sensor event */
  sensors_event_t event;
  accel.getEvent(&event);
  /* Display the results (acceleration is measured in m/s^2) */
  lcd.clear();
  lcd.setCursor(0, 0); // Set the cursor on the third column and first row.
  lcd.print("Accelerometer");
  String string_values = "X:" + String(event.acceleration.x);
  string_values += "  Y:" + String(event.acceleration.y);
  lcd.setCursor(0, 1);
  lcd.print(string_values);
  string_values = "Z:" + String(event.acceleration.z);
  lcd.setCursor(0, 2);
  lcd.print(string_values);
  lcd.setCursor(0, 3);
  lcd.print("m/s^2  I: " + String(val));
}

void do_intensity(char val) {
  // Intensity 1
  if (val == '1') {
    // change the angle for next time through the loop:
    for (angle = 90; angle < 120; angle++) {
      myservo.write(angle);
    }
    for (angle2 = 120; angle2 > 90; angle2--) {
      myservo2.write(angle);
      delay(15);
    }
    // now scan back from 180 to 0 degrees
    for (angle = 120; angle > 90; angle--) {
      myservo.write(angle);
    }
    for (angle2 = 90; angle2 < 120; angle2++) {
      myservo2.write(angle);
      delay(15);
    }
  }

  // Intensity 2
  if (val == '2') {
    for (angle = 90; angle < 120; angle++) {
      myservo.write(angle);
    }
    for (angle2 = 120; angle2 > 90; angle2--) {
      myservo2.write(angle2);
      delay(10);
    }
    for (angle = 120; angle > 90; angle--) {
      myservo.write(angle);
    }
    for (angle2 = 90; angle2 < 120; angle2++) {
      myservo2.write(angle2);
      delay(10);
    }
  }

  // Intensity 3
  if (val == '3') {
    for (angle = 90; angle < 120; angle++) {
      myservo.write(angle);
    }
    for (angle2 = 120; angle2 > 90; angle2--) {
      myservo2.write(angle2);
      delay(5);
    }
    for (angle = 120; angle > 90; angle--) {
      myservo.write(angle);
    }
    for (angle2 = 90; angle2 < 120; angle2++) {
      myservo2.write(angle2);
      delay(5);
    }
  }
}

void loop() {
  // Button Start
  if (digitalRead(pushButtonPin1) == LOW) {
    Serial.println("Started.");
    buttonPushed1 = 1;
    buttonPushed2 = 0;
  } if (buttonPushed1) {
    Serial.println("Simulating...");
    // Read from serial
    if (Serial.available()) {
      val = Serial.read();
      do_intensity(val);
    }
    show_values();
  }

  // Button Stop
  if (digitalRead(pushButtonPin2) == LOW) {
    Serial.println("Stopped.");
    buttonPushed2 = 1;
    buttonPushed1 = 0;
  } if (buttonPushed2) {
    welcome_message();
  }
}
