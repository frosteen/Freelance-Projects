int sensorPin = A0;
int PWM = 3;
int sensorVal;
int PWMVal;

float R1 = 10000;
float logR2, R2, T;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

void setup() {
  // put your setup code here, to run once:
  pinMode(sensorPin, INPUT);
  pinMode(PWM, OUTPUT);
  Serial.begin(9600);

  
}

void loop() {

  sensorVal = analogRead(sensorPin);
  R2 = R1 * (1023.0 / (float)sensorVal - 1.0);s
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  // put your main code here, to run repeatedly:
  //this code prints sensor value to the console

  //read sensor value and set upper limit cap
  sensorVal = analogRead(sensorPin);
  if(T >50){
    T = 50;
  }

  //map and assign pwm values to the fan output 0 to 255 corresponds to 0 to 100%
  PWMVal = map(T, 49,50, 225, 40);

  //set 450 as out cutout or cut in limit where the fan switches from off to the lower PWM limit
  if(T <40){
    PWMVal = 0;
  }

  //write the PWM value to the pwm output pin
  analogWrite(PWM, PWMVal);

//  Serial.print("Temperature: "); 
  Serial.println(T);
//  Serial.println(" C"); 
    delay(100);
}
