#include <Q2HX711.h>
#include "max6675.h"

/* 
*   Rheometer arduino python interface
*   Nov/09/2017 sketch version 1.4
*   
*/

// Pin assignments
const byte emrg_sw = 2;
const byte mag_sw = 3;
// These two pins (2,3) are interrupt capable
const byte th0CS = 4;
const byte th0DO = 5;
const byte th0CLK = 6;
const byte th1CS = 7;
byte th1DO = th0DO;       // SDA (parallel i2c connection)
byte th1CLK = th0CLK;     // SCL (parallel i2c connection)
const byte hx711_DO = 8;
const byte hx711_CK = 9;
const byte relay1 = 10;
const byte relay2 = 11;
const byte relay3 = 12;
const byte relay4 = A0;
const byte relay5 = A1;
const byte relay6 = A2;


// Sensing Module objects
Q2HX711 hx711(hx711_DO, hx711_CK);
MAX6675 t_couple0(th0CLK, th0CS, th0DO);
MAX6675 t_couple1(th1CLK, th1CS, th1DO);


// Global constants
float th0_val = 0.0;
float th1_val = 0.0;
unsigned long time_in = millis();
String s_output = "";
boolean send_data_FLAG = false;
boolean em_stop_FLAG = false;
boolean relay1_STATUS = false;
boolean relay2_STATUS = false;
boolean relay3_STATUS = false;
boolean relay4_STATUS = false;
boolean relay5_STATUS = false;
boolean relay6_STATUS = false;
boolean relay1_SAVE = false;
boolean relay2_SAVE = false;
boolean relay3_SAVE = false;
boolean relay4_SAVE = false;
boolean relay5_SAVE = false;
boolean relay6_SAVE = false;


void setup() {
  // General Inputs
  pinMode(emrg_sw, INPUT_PULLUP);
  pinMode(mag_sw, INPUT_PULLUP);
  // General Outputs
  pinMode(relay1, OUTPUT);
  digitalWrite(relay1, HIGH);
  pinMode(relay2, OUTPUT);
  digitalWrite(relay2, HIGH);
  pinMode(relay3, OUTPUT);
  digitalWrite(relay3, HIGH);
  pinMode(relay4, OUTPUT);
  digitalWrite(relay4, HIGH);
  pinMode(relay5, OUTPUT);
  digitalWrite(relay5, HIGH);
  pinMode(relay6, OUTPUT);
  digitalWrite(relay6, HIGH);
  // Serial interface initializartion
  Serial.begin(115200);
  // Wait for MAX6675 temperature modules to initialize
  delay(1000);
  t_couple0.readCelsius();
  t_couple1.readCelsius();
  attachInterrupt(0,emergency_stop_ISR, FALLING);
  // wait for python to intiate the transfer
  while (Serial.available() == 0) {}
}


void emergency_stop_ISR() {
  unsigned long time_st;
  digitalWrite(relay1, HIGH);
  digitalWrite(relay2, HIGH);
  digitalWrite(relay3, HIGH);
  digitalWrite(relay4, HIGH);
  digitalWrite(relay5, HIGH);
  digitalWrite(relay6, HIGH);
  if (em_stop_FLAG == false) {
    relay6_SAVE = relay6_STATUS;
    relay5_SAVE = relay5_STATUS;
    relay4_SAVE = relay4_STATUS;
    relay3_SAVE = relay3_STATUS;
    relay2_SAVE = relay2_STATUS;
    relay1_SAVE = relay1_STATUS;
    em_stop_FLAG == true;
    time_st = millis();
    }
  while (digitalRead(2) == LOW) {
    if ((time_st - millis()) >= 250) {
      Serial.print("N/A");
      Serial.print(' ');
      Serial.print("N/A");
      Serial.print(' ');
      Serial.print("N/A");
      Serial.print(' ');
      Serial.print(!(digitalRead(emrg_sw)));
      Serial.print(!(digitalRead(mag_sw)));
      Serial.print(relay6_STATUS);
      Serial.print(relay5_STATUS);
      Serial.print(relay4_STATUS);
      Serial.print(relay3_STATUS);
      Serial.print(relay2_STATUS);
      Serial.println(relay1_STATUS);
      time_st = millis();
      }
    }
    if (relay6_SAVE == false) { digitalWrite(relay6, HIGH); }
    else {digitalWrite(relay6, LOW); }
    if (relay5_SAVE == false) { digitalWrite(relay5, HIGH); }
    else {digitalWrite(relay5, LOW); }
    if (relay4_SAVE == false) { digitalWrite(relay4, HIGH); }
    else {digitalWrite(relay4, LOW); }
    if (relay3_SAVE == false) { digitalWrite(relay3, HIGH); }
    else {digitalWrite(relay3, LOW); }
    if (relay2_SAVE == false) { digitalWrite(relay2, HIGH); }
    else {digitalWrite(relay2, LOW); }
    if (relay1_SAVE == false) { digitalWrite(relay1, HIGH); }
    else {digitalWrite(relay1, LOW); }
    em_stop_FLAG == false;
  }


void send_data() {
  // This function sends all readings through the
  // serial port, as fast as possible. MAX6675 need
  // 0.3 seconds to generate valid readings
  if ((millis() - time_in) >= 300 ) {
    th0_val = t_couple0.readCelsius();
    th1_val = t_couple1.readCelsius();
    time_in = millis();
  }
  Serial.print(hx711.read());
  Serial.print(' ');
  Serial.print(th0_val);
  Serial.print(' ');
  Serial.print(th1_val);
  Serial.print(' ');
  Serial.print(!(digitalRead(emrg_sw)));
  Serial.print(!(digitalRead(mag_sw)));
  Serial.print(relay6_STATUS);
  Serial.print(relay5_STATUS);
  Serial.print(relay4_STATUS);
  Serial.print(relay3_STATUS);
  Serial.print(relay2_STATUS);
  Serial.println(relay1_STATUS);
  }


void serialEvent() {
  // Decode input received from serial
  // This function is called everytime the serial
  // buffer has data pending to be read
  char input = (char)Serial.read();
  switch (input) {
    case '0': send_data_FLAG = false;
              break;
    case '1': send_data_FLAG = true;
              break;
    case '2': digitalWrite(relay1, HIGH);
              relay1_STATUS = false;
              break;
    case '3': digitalWrite(relay1, LOW);
              relay1_STATUS = true;
              break;
    case '4': digitalWrite(relay2, HIGH);
              relay2_STATUS = false;
              break;
    case '5': digitalWrite(relay2, LOW);
              relay2_STATUS = true;
              break;
    case '6': digitalWrite(relay3, HIGH);
              relay3_STATUS = false;
              break;
    case '7': digitalWrite(relay3, LOW);
              relay3_STATUS = true;
              break;
    case '8': digitalWrite(relay4, HIGH);
              relay4_STATUS = false;
              break;    
    case '9': digitalWrite(relay4, LOW);
              relay4_STATUS = true;
              break;    
    case 'a': digitalWrite(relay5, HIGH);
              relay5_STATUS = false;
              break;    
    case 'b': digitalWrite(relay5, LOW);
              relay5_STATUS = true;
              break;    
    case 'c': digitalWrite(relay6, HIGH);
              relay6_STATUS = false;
              break;    
    case 'd': digitalWrite(relay6, LOW);
              relay6_STATUS = true;
              break;    
    default:  Serial.print("Invalid data received: ");
              Serial.println(input);
              break;
    }
}


void loop() {
    if (send_data_FLAG == true) { send_data(); }   
}
