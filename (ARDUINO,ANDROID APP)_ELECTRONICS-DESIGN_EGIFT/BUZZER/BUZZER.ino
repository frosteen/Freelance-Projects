/*************************************************
 * Public Constants
 *************************************************/

#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978

int pulsantePin = 7;
int pulsanteStato;
int attesaDebounce = 50;
unsigned long ultimoTempoDebounce = 0;
int ultimaLettura = LOW;
int ripetizione = 6;
int buzzerPin = D3;
int canzoni [6][50]={{
  // Jingle Bells
  NOTE_E5, NOTE_E5, NOTE_E5,
  NOTE_E5, NOTE_E5, NOTE_E5,
  NOTE_E5, NOTE_G5, NOTE_C5, NOTE_D5,
  NOTE_E5,
  NOTE_F5, NOTE_F5, NOTE_F5, NOTE_F5,
  NOTE_F5, NOTE_E5, NOTE_E5, NOTE_E5, NOTE_E5,
  NOTE_E5, NOTE_D5, NOTE_D5, NOTE_E5,
  NOTE_D5, NOTE_G5
},{
  8, 8, 4,
  8, 8, 4,
  8, 8, 8, 8,
  2,
  8, 8, 8, 8,
  8, 8, 8, 16, 16,
  8, 8, 8, 8,
  4, 4
},{
  // We wish you a merry Christmas
  NOTE_B3, 
  NOTE_F4, NOTE_F4, NOTE_G4, NOTE_F4, NOTE_E4,
  NOTE_D4, NOTE_D4, NOTE_D4,
  NOTE_G4, NOTE_G4, NOTE_A4, NOTE_G4, NOTE_F4,
  NOTE_E4, NOTE_E4, NOTE_E4,
  NOTE_A4, NOTE_A4, NOTE_B4, NOTE_A4, NOTE_G4,
  NOTE_F4, NOTE_D4, NOTE_B3, NOTE_B3,
  NOTE_D4, NOTE_G4, NOTE_E4,
  NOTE_F4
},{
  4,
  4, 8, 8, 8, 8,
  4, 4, 4,
  4, 8, 8, 8, 8,
  4, 4, 4,
  4, 8, 8, 8, 8,
  4, 4, 8, 8,
  4, 4, 4,
  2
},{
  // Santa Claus is coming to town
  NOTE_G4,
  NOTE_E4, NOTE_F4, NOTE_G4, NOTE_G4, NOTE_G4,
  NOTE_A4, NOTE_B4, NOTE_C5, NOTE_C5, NOTE_C5,
  NOTE_E4, NOTE_F4, NOTE_G4, NOTE_G4, NOTE_G4,
  NOTE_A4, NOTE_G4, NOTE_F4, NOTE_F4,
  NOTE_E4, NOTE_G4, NOTE_C4, NOTE_E4,
  NOTE_D4, NOTE_F4, NOTE_B3,
  NOTE_C4
},{
  8,
  8, 8, 4, 4, 4,
  8, 8, 4, 4, 4,
  8, 8, 4, 4, 4,
  8, 8, 4, 2,
  4, 4, 4, 4,
  4, 2, 4,
  1
}};

String messaggi[] = {
  "Merry Christmas",
  "Buon Natale",
  "Joyeux Noel",
  "Shub Naya Baras",
  "Feliz Navidad"
};

int numeroNote = 26;
int led[] = {2,3,4,5};
int lettura = LOW;
 
int pos = 0;
int w = 0;

// the setup routine runs once when you press reset:
void setup() { 
  pinMode(buzzerPin, OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  suona();
}

void illumina(){                      // wait for 1/2 a second
  digitalWrite(led[0], LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(led[1], HIGH);    // turn the LED on (HIGH is the voltage level)
  delay(150);                      // wait for 1/2 a second
  digitalWrite(led[1], LOW);     // turn the LED off by making the voltage LOW
  digitalWrite(led[2], HIGH);     // turn the LED on (HIGH is the voltage level)
  delay(150);                      // wait for 1/2 a second
  digitalWrite(led[2], LOW);      // turn the LED off by making the voltage LOW
  digitalWrite(led[3], HIGH);     // turn the LED on (HIGH is the voltage level)
  delay(150);                      // wait for 1/2 a second
  digitalWrite(led[3], LOW);      // turn the LED off by making the voltage LOW
  digitalWrite(led[2], HIGH);      // turn the LED off by making the voltage LOW
  delay(150); 
  digitalWrite(led[2], LOW);      // turn the LED off by making the voltage LOW
  digitalWrite(led[1], HIGH);      // turn the LED off by making the voltage LOW
  delay(150); 
  digitalWrite(led[1], LOW);      // turn the LED off by making the voltage LOW
  digitalWrite(led[0], HIGH);      // turn the LED off by making the voltage LOW
  delay(150);   
}

void suona(){
  int pos = 180;
  int m = 0;
  int n = 0;
  int z = 0;
  int pari;
  if(ripetizione==6 || ripetizione == 2){
     pari = 0;
  }
  else if(ripetizione==0){
    pari = 4;
  }
  else if(ripetizione==4){
    pari = 2;
  }
  
  int dispari= pari+1;
  for(int i = 0; i < numeroNote; i++){
    delay(80);
    m = random(0,4);
    n = random(0,4);
    int durata = 1500 / canzoni[dispari][i];
    tone(buzzerPin, canzoni[pari][i], durata); 
    delay(durata * 1.3);
    pos = pos -7;
    z++;
    if(z==5){
      z=0;
    }
 }
 ripetizione = pari;  
}
