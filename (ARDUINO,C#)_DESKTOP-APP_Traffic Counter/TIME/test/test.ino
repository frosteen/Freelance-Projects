void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(D1, OUTPUT);
  delay(3000);
  digitalWrite(D1,HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (analogRead(A0) >= 50) {
    Serial.println("Working!");
  }
  digitalWrite(D1,HIGH);
}
