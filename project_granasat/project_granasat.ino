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



#define IR_INPUT_PIN    2 //IR receiver output
// Include for InfraRed Signal Library (Remote)
#include "IRremote-3.7.0/src/TinyIRReceiver.hpp"

#include "musiclights.h"  // library contating the notes and delay of the music


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

int starting_time;
int current_time;
int playing_song;
int current_note;
int delay_on_lights [32];
uint8_t pinValues [4];
const int * start_array;
const int * light_array;
const int * delay_array;
int total_notes;

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
  starting_time = millis()/10;
  current_note = 0;
  playing_song = 1;

  //Setting dealy_on_lights to 0
  for (int i=0;i<32;i++){
    delay_on_lights[i] = 0;
  }

}

//(WIP) Añadir las funciones de optimizadores 


void loop()
{

  //Set the arrays acording to the song you want to play
  switch(playing_song){
    case 1: 
      start_array = start1;
      delay_array = delay1;
      light_array = light1;
      total_notes = notes1;
      playing_song = 0;
      break;
    case -1:
      break;
  }

  //If a song is playing, run the code
  if (playing_song != -1){
    //Check the current time since the song started
    current_time = millis()/10 - starting_time;
    //Check when the next light will turn on
    int current_start = pgm_read_word_near(start_array+current_note);
    //Check when it will shut off after it turns on
    int current_delay = pgm_read_word_near(delay_array+current_note);
    //Chech which light will turn on
    int current_light = pgm_read_word_near(light_array+current_note);

    //If a note should start, run this code
    while(current_start < current_time && total_notes > current_note){
      //Turn on the light for current_delay time
      delay_on_lights[current_light] = current_time+current_delay;
      //Check the next note
      current_note++;
      if (total_notes > current_note){
        current_start = pgm_read_word_near(start_array+current_note);
        current_delay = pgm_read_word_near(delay_array+current_note);
        current_light = pgm_read_word_near(light_array+current_note);
      }
      else //If no more notes are left, stop playing the song
        playing_song = -1;
    }
    //Check if any lights should be turn off
    for (int i =0;i<32;i++){
      if (delay_on_lights[i] <= current_time){
        delay_on_lights[i] = 0;
      }
    }

    //This is a temporal workaround for the buggy board
    delay_on_lights[24] = 1000;
    //Turn on all the lights
    turnOnLights(delay_on_lights,pinValues);
  }
  //Timer between iterations
  delay(10);

}

//Turn on all lights given in the lights array and turn off all others.
void turnOnLights(int * lights,uint8_t * pinValues){
  //Set pinValues to blank
  pinValues[0] = { 0b00000000 };
  pinValues[1] = { 0b00000000 };
  pinValues[2] = { 0b00000000 };
  pinValues[3] = { 0b00000000 };

  //For each light position
  for (int i = 0; i < 32;i++){
    int pos = i;
    //If light is greater than 0, turn on the bit representing that light in pinValues
    if (lights[pos] > 0){
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
  //Turn on all the lights
  sr.setAll(pinValues);

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
