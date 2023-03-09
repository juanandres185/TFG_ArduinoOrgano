#include "lin.h"


// Standard arduino settings
#define LED 13
#define LED_ON HIGH
#define TX_PIN 3
#define RX_PIN 4
#define ENABLE_PIN 10

Lin lin(Serial, TX_PIN);



void setup() {
  // put your setup code here, to run once:
  lin.begin(19200);

  pinMode(LED, OUTPUT);
  digitalWrite(LED, !LED_ON);
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, HIGH);
}

unsigned long t = 0;

void delay_until(unsigned long ms) {
  unsigned long end = t + (1000 * ms);
  unsigned long d = end - micros();

  // crazy long delay; probably negative wrap-around
  // just return
  if ( d > 1000000 ) {
    t = micros();
    return;
  }
  
  if (d > 15000) {
    unsigned long d2 = (d-15000)/1000;
    delay(d2);
    d = end - micros();
  }
  delayMicroseconds(d);
  t = end;
}


void loop() {
  // put your main code here, to run repeatedly:
  //uint8_t empty[] = { 0, 1, 2 };

  // Send ID 11
    byte BZ;
  
    byte dynamic_ON1[8] = {0x00, 0x01 << 8 | BZ, 0x00, 0x00, 0x00, 0x10, 0x0E, 0x00};
    
    lin.send(0x0A, dynamic_ON1, 8, 2);
    BZ++;
    delay(10);

    lin.send(0x0B, dynamic_ON1, 8, 2);
    delay(10);
 


    //byte dynamic_ON2[8] = {0x00, 0x01 << 8 | BZ, 0x00, 0x00, 0x00, 0x10, 0x0E, 0x00};

    lin.send(0x0A, dynamic_ON1, 8, 2);
    BZ++;
    delay(10);

    lin.send(0x0C, dynamic_ON1, 8, 2);
    delay(10);


    //byte dynamic_ON3[8] = {0x00, 0x01 << 8 | BZ, 0x00, 0x00, 0x00, 0x10, 0x0E, 0x00};

    lin.send(0x0A, dynamic_ON1, 8, 2);
    BZ++;
    delay(10);

    lin.send(0x0D, dynamic_ON1, 8, 2);
    delay(10);


    //byte dynamic_ON4[8] = {0x00, 0x01 << 8 | BZ, 0x00, 0x00, 0x00, 0x10, 0x0E, 0x00};

    lin.send(0x0A, dynamic_ON1, 8, 2);
    BZ++;
    delay(10);

    lin.send(0x0E, dynamic_ON1, 8, 2);
    delay(10);

   
    /*
    lin.send(0x00, 0, 0, 2);
    delay_until(5000);
    lin.send(0x10, 0, 0, 2);
    delay_until(5000);
    lin.send(0x0E, 0, 0, 2);
    delay_until(5000);
    lin.send(0x0D, 0, 0, 2);
    delay_until(5000);
  */


  
}
