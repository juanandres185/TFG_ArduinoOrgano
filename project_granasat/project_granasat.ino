#include <Arduino.h>
#include <Wire.h>

// Include Shift Register Library
#include "ShiftRegister74HC595/src/ShiftRegister74HC595.h"
#include "ShiftRegister74HC595/src/ShiftRegister74HC595.cpp"

// Include Clock
#include "ArduinoRTClibrary-master/virtuabotixRTC.h"
#include "ArduinoRTClibrary-master/virtuabotixRTC.cpp"

// Include MP3 Pin Library
#include "AltSoftSerial/AltSoftSerial.h"
#include "AltSoftSerial/AltSoftSerial.cpp"

// Include MP3 Player Library
#include "DFRobotDFPlayerMini-master/DFRobotDFPlayerMini.h"
#include "DFRobotDFPlayerMini-master/DFRobotDFPlayerMini.cpp"

// Include Display Graphic Library
#include "Adafruit_GFX_Library/Adafruit_GFX.h"
#include "Adafruit_GFX_Library/Adafruit_GFX.cpp"
#include "Adafruit_SSD1306/Adafruit_SSD1306.h"
#include "Adafruit_SSD1306/Adafruit_SSD1306.cpp"



// Include for InfraRed Signal Library (Remote)
#include "IRremote-3.7.0/src/TinyIRReceiver.hpp"

#include "musiclights.h"  // library contating the notes and delay of the music

#define IR_INPUT_PIN    2 //IR receiver output

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C // 0x3D for 128x64, 0x3C for 128x32

// pins for the shift register
#define serialDataPin 7 
#define clockPin 12
#define latchPin 11 

#define OutputEnableLED 13

#define NumberOf74HC595 4 
#define LedPin 13 

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

ShiftRegister74HC595<NumberOf74HC595> sr(serialDataPin, clockPin, latchPin);

// definition of the hex codes of the signal from IR remote
#define ONE 0x0
#define TWO 0x1
#define THREE 0x2
#define FOUR 0x4
#define FIVE 0x5
#define SIX 0x6
#define SEVEN 0x8
#define EIGHT 0x9
#define NINE 0xA
#define STAR 0xC
#define ZERO 0xD
#define HASH 0xE
#define LEFT 0x14
#define OKAY 0x15
#define RIGHT 0x16
#define UP 0x11
#define DOWN 0x19

//Definition of max and min volume
int vol = 25;
int minvol = 0;
int maxvol = 40;

static const uint8_t PIN_MP3_TX = 9; // Connects to module's RX 
static const uint8_t PIN_MP3_RX = 8; // Connects to module's TX 
AltSoftSerial softwareSerial(PIN_MP3_RX, PIN_MP3_TX);

// Creation of the DFPlayer object
DFRobotDFPlayerMini player;

#if !defined(STR_HELPER)
#define STR_HELPER(x) #x
#define STR(x) STR_HELPER(x)
#endif

volatile struct TinyIRReceiverCallbackDataStruct sCallbackData;

// Inicialization clock DS1302
#define CLK 14
#define DAT 15
#define RST 16
virtuabotixRTC myRTC(CLK, DAT, RST);


void setup()
{
  //Pin initialization
  pinMode(serialDataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(OutputEnableLED, OUTPUT);
  analogWrite(OutputEnableLED, 0);

  //Audio player initialization
  Serial.begin(9600);
  softwareSerial.begin(9600);
  if (player.begin(softwareSerial)) {
    Serial.println(F("OK dfplayer"));
    player.volume(vol); // Set volume
  }
  else {
    Serial.println(F("Connecting to DFPlayer Mini failed!"));
  }

  //Remote controller initialization
  initPCIInterruptForTinyReceiver(); //WIP
  Serial.println(F("Ready to receive IR signals at pin " STR(IR_INPUT_PIN)));

  //Display initialization
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32 display
    Serial.println(F("SSD1306 allocation failed"));
  }
  delay(2000);

  //display settings
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);

  display.clearDisplay();
  display.setTextSize(2); // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(15, 10);
  display.display();      // Show initial text

  // init clock
  myRTC.setDS1302Time(00, 20, 13, 3, 8, 3, 2023);
  
}

//(WIP) Añadir las funciones de optimizadores 
int cur_note = 0;
int new_delay = 0;


void loop()
{
  uint8_t pinValues[] = {0b0000};
  int luces[] = {24,0};
  int num_luces = sizeof(luces) / sizeof(int);

  luces[1] = pgm_read_word(&light1[cur_note]);
  new_delay = pgm_read_word(&delay1[cur_note]);

  delay(new_delay);
  enciendeLuces(luces,num_luces,pinValues);

  sr.setAll(pinValues);
  cur_note = cur_note +1;
  myRTC.updateTime();
  if (cur_note > notes1){
    cur_note = 0;
  }
}


void enciendeLuces(int * luces,int num_luces,uint8_t * pinValues){
  pinValues[0] = { 0b00000000 };
  pinValues[1] = { 0b00000000 };
  pinValues[2] = { 0b00000000 };
  pinValues[3] = { 0b00000000 };

  for (int i = 0; i < num_luces;i++){
    int pos = luces[i];

    uint8_t mask = 0b00000001;

    if (pos < 8){
      mask = mask << pos;
      pinValues[3] = ( pinValues[3] | mask);
    }
    else if(pos >=8 && pos < 16) {
      mask = mask << (pos % 8);
      pinValues[1] = ( pinValues[1] | mask);
    }
    else if (pos >= 16 && pos < 24){
      mask = mask << ((pos+1)%8);
      pinValues[2] = ( pinValues[2] | mask);
    }
    else if (pos >= 24 && pos < 32){
      mask = mask << ((pos+1)%8);
      pinValues[0] = ( pinValues[0] | mask);
    }
  }
}


// void displayAll(void){

//   //Fecha

//   //Actualizar el reloj
//   myRTC.updateTime();
//   //Resetear el display
//   display.clearDisplay();
//   display.setTextSize(2); // Draw 2X-scale text
//   display.setTextColor(SSD1306_WHITE);
//   display.setCursor(15, 10);
//   //Mostrar la fecha
//   display.print(myRTC.dayofmonth);
//   display.print(F("/"));
//   display.print(myRTC.month);
//   display.print(F("/"));
//   display.print(myRTC.year);
//   display.display();      // Show initial text
//   delay(100);
  
//   // Scroll in the text
//   display.startscrollright(0x00, 0x0F);
//   delay(2250);
//   display.stopscroll();
//   delay(1000);

//   //Hora

//   //Actualizar el reloj
//   myRTC.updateTime();
//   //Limpiar el display
//   display.clearDisplay();
//   display.setTextSize(2); // Draw 2X-scale text
//   display.setTextColor(SSD1306_WHITE);
//   display.setCursor(15, 10);
//   //Mostrar la fecha y hora
//   display.print(myRTC.hours);
//   display.print(F(":"));
//   display.print(myRTC.minutes);
//   display.print(F(":"));
//   display.print(myRTC.seconds);
//   display.display();      // Show initial text
//   delay(100);
  

//   // Scroll in the text
//   display.startscrollright(0x00, 0x0F);
//   delay(2250);
//   display.stopscroll();
//   delay(1000);

// }

// void testscrolltext(void) {

//   display.clearDisplay();
//   display.setTextSize(2); // Draw 2X-scale text
//   display.setTextColor(SSD1306_WHITE);
//   display.setCursor(15, 10);
//   display.println(F("GranaSAT"));
//   display.display();      // Show initial text
//   delay(100);

//   // Scroll in the text
//   display.startscrollright(0x00, 0x0F);
//   delay(2250);
//   display.stopscroll();
//   delay(1000);
  
// }

// interrupt for IR and getting the hexcode for the commands
#if defined(ESP8266) || defined(ESP32)
  void IRAM_ATTR handleReceivedTinyIRData(uint16_t aAddress, uint8_t aCommand, bool isRepeat)
#else
  void handleReceivedTinyIRData(uint16_t aAddress, uint8_t aCommand, bool isRepeat)
#endif
{
  #if defined(ARDUINO_ARCH_MBED) || defined(ESP32)
    // Copy data for main loop, this is the recommended way for handling a callback :-)
    sCallbackData.Address = aAddress;
    sCallbackData.Command = aCommand;
    sCallbackData.isRepeat = isRepeat;
    sCallbackData.justWritten = true;
  #else

    // Print the codes
    Serial.print(F("A=0x"));
    Serial.print(aAddress, HEX);
    Serial.print(F(" C=0x"));
    Serial.print(aCommand, HEX);
    Serial.print(F(" R="));
    Serial.print(isRepeat);
    Serial.println();
    
    // various actions for different buttons
    switch(aCommand)
    {
      case ONE  : display.clearDisplay();display.setCursor(0,0);Serial.println(F("1 is pressed"));display.println("Mozart: Sonata 16");display.setCursor(5,15);display.print("Volume:"); display.println(vol);display.display(); player.play(1); break;
      case TWO  : display.clearDisplay();display.setCursor(0,0);Serial.println(F("2 is pressed"));display.println("Beethoven: Minuet");display.setCursor(5,15);display.print("Volume:"); display.println(vol);display.display(); player.play(2); break;
      case THREE  : display.clearDisplay();display.setCursor(0,0);Serial.println(F("3 is pressed"));display.println("Beethoven: Fur Elise");display.setCursor(5,15);display.print("Volume:"); display.println(vol);display.display(); player.play(3); break;
      case FOUR : display.clearDisplay();display.setCursor(0,0);Serial.println(F("4 is pressed"));display.println("Einaudi: Nuvole Bianche");display.setCursor(5,15);display.print("Volume:"); display.println(vol);display.display(); player.play(4); break;
      case FIVE : display.clearDisplay();display.setCursor(0,0);Serial.println(F("5 is pressed"));display.println("The Beatles: Hey Jude");display.setCursor(5,15);display.print("Volume:"); display.println(vol);display.display(); player.play(5); break;
      case SIX  : display.clearDisplay();display.setCursor(0,0);Serial.println(F("6 is pressed"));display.println("John Denver: Country Roads");display.setCursor(5,15);display.print("Volume:"); display.println(vol);display.display(); player.play(6); break;
      case SEVEN  : display.clearDisplay();display.setCursor(0,0);Serial.println(F("7 is pressed"));display.println("Queen: Bohemian Rhapsody");display.setCursor(5,15);display.print("Volume:"); display.println(vol);display.display(); player.play(7); break;
      case EIGHT  : display.clearDisplay();display.setCursor(0,0);Serial.println(F("8 is pressed"));display.println("8");display.display(); display.println(vol); player.play(8); break;
      case NINE :  display.clearDisplay();display.setCursor(0,0);Serial.println(F("9 is pressed"));display.println("9");display.display(); player.play(9); break;
      case UP : vol = vol +1; if(vol>40){vol = maxvol;} player.volume(vol);display.clearDisplay();display.setCursor(5,15);Serial.println("UP is pressed");display.print("Volume:"); display.println(vol);display.display(); break;
      case DOWN : vol = vol -1; if (vol<0){vol = minvol;} player.volume(vol);display.clearDisplay();display.setCursor(5,15);Serial.println("DOWN is pressed");display.print("Volume:"); display.println(vol);display.display(); break;
      case LEFT : Serial.println(F("LEFT is pressed")); break;
      case RIGHT  : Serial.println(F("RIGHT is pressed")); break;
      case OKAY : Serial.println(F("OK is pressed")); break;
      case ZERO : Serial.println(F("0 is pressed")); break;
      case STAR : Serial.println(F("STAR is pressed")); break;
      case HASH : Serial.println(F("HASH is pressed")); break;
      default: 
      Serial.println(" other button : ");
      Serial.println(aCommand, HEX);
      for (int i = 1; i<8 ; i++){
        player.play(i);
      }
    }// End Case
    
  #endif
}
