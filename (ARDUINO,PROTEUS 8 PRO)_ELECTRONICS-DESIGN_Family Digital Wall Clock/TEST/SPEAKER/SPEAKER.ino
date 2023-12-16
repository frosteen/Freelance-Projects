#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"
//Inicia a serial por software nos pinos 10 e 11
SoftwareSerial mySoftwareSerial(5, 6); // RX, TX
//Objeto responsável pela comunicação com o módulo MP3 (DFPlayer Mini)
DFRobotDFPlayerMini myDFPlayer;
//variável responsável por armazenar os comandos enviados para controlar o player
String buf;
//variável responsável por armazenar o estado do player (0: tocando ; 1: pausado)
boolean pausa = false;
//variável responsável por armazenar o estado da equalização
//varia de 0 a 5
int equalizacao = 0; // (0 = Normal, 1 = Pop, 2 = Rock, 3 = Jazz, 4 = Classic, 5 = Bass)"
//variável responsável por armazenar o total de músicas presentes no SD card.
int maxSongs = 0;
void setup()
{
  //Comunicacao serial com o modulo
  mySoftwareSerial.begin(9600);
  //Inicializa a serial do Arduino
  Serial.begin(115200); //Verifica se o modulo esta respondendo e se o
  //cartao SD foi encontrado
  Serial.println();
  Serial.println("DFRobot DFPlayer Mini");
  Serial.println("Initiliaizing DFPlayer... (3~5 seconds)");
  if (!myDFPlayer.begin(mySoftwareSerial))
  {
    Serial.println("Not initialized:");
    Serial.println("1.Check the DFPlayer Mini connections");
    Serial.println("2.Insert an SD card");
    while (true);
  }
  Serial.println();
  Serial.println("DFPlayer Mini module initialized!");

  //Definicoes iniciais
  myDFPlayer.setTimeOut(500); //Timeout serial 500ms
  myDFPlayer.volume(30); //Volume 10     vai de 0 a 30
  myDFPlayer.EQ(5); //Equalizacao normal
  //recupera o numero de Músicas encontradas no SD.
  maxSongs = myDFPlayer.readFileCounts(DFPLAYER_DEVICE_SD);
  Serial.println();
  Serial.print("Number of files on the SD card: ");
  Serial.println(maxSongs);
  //Mostra o menu de comandos 
  menu_opcoes();
}
void menu_opcoes()
{
  Serial.println();
  Serial.println("Commands:");
  Serial.print(" [1-");
  Serial.print(maxSongs);
  Serial.println("] To select the MP3 file");
  Serial.println(" [s] Stop Playing");
  Serial.println(" [p] pause / continue music");
  Serial.println(" [e] selects equalization");
  Serial.println(" [+ or -] increases or decreases the volume");
  Serial.println();
}

void loop()
{
  //Aguarda a entrada de dados pela serial
  while (Serial.available() > 0)
  {
    //recupera os dados de entrada
    buf = Serial.readStringUntil('\n');
    //Reproducao (índice da música)
    if ((buf.toInt() >= 1) && (buf.toInt() <= maxSongs))
    {
      Serial.print("Playing music: ");
      Serial.println(buf.toInt());
      myDFPlayer.play(buf.toInt()); // dá play na música
      menu_opcoes();
    }
    //Pausa/Continua a musica
    if (buf == "p")
    {
      if (pausa)
      {
        Serial.println("Continue music...");
        myDFPlayer.start();
      }
      else
      {
        Serial.println("Music paused...");
        myDFPlayer.pause();
      }
      pausa = !pausa;

      menu_opcoes();
    }

    //Parada
    if (buf == "s")
    {
      myDFPlayer.stop();
      Serial.println("Music stopped!");
      menu_opcoes();
    }

    //Seleciona equalizacao
    if (buf == "e")
    {
      equalizacao++;
      if (equalizacao == 6)
      {
        equalizacao = 0;
      }
      myDFPlayer.EQ(equalizacao);
      Serial.print("Equalization: ");
      Serial.print(equalizacao);
      Serial.println(" (0 = Normal, 1 = Pop, 2 = Rock, 3 = Jazz, 4 = Classic, 5 = Bass)");
      menu_opcoes();
    }

    //Aumenta volume
    if (buf == "+")
    {
      myDFPlayer.volumeUp();
      Serial.print("Volume current:");
      Serial.println(myDFPlayer.readVolume());
      menu_opcoes();
    }
    //Diminui volume
    if (buf == "-")
    {
      myDFPlayer.volumeDown();
      Serial.print("Volume current:");
      Serial.println(myDFPlayer.readVolume());
      menu_opcoes();
    }
  } //while
} //loop`
