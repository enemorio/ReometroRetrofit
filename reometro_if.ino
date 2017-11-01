#include <Q2HX711.h>
#include "max6675.h"

const byte hx711_data_pin = 8;
const byte hx711_clock_pin = 9;
int mag_sw = 7;
int thermoDO = 5;
int thermoCS = 4;
int thermoCLK = 6;

Q2HX711 hx711(hx711_data_pin, hx711_clock_pin);
MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

float loadcell_val = 0.0;
float thermo0_val = 0.0;
boolean sw_val = false;
unsigned long time_in = millis();
String s_output = "";

void setup() {
  Serial.begin(115200);
  pinMode(mag_sw, INPUT_PULLUP);
  pinMode(10, OUTPUT);
  digitalWrite(10, HIGH);
  pinMode(11, OUTPUT);
  digitalWrite(11, HIGH);
  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  delay(1000);
  thermo0_val = thermocouple.readCelsius();
}

void loop() {
  loadcell_val = hx711.read()/8.75 - 981620;
  sw_val = digitalRead(mag_sw);
  if ((millis() - time_in) >= 500 ) {
    thermo0_val = thermocouple.readCelsius();
    time_in = millis();
  }
  Serial.print(!sw_val);
  Serial.print(' ');
  Serial.print(loadcell_val);
  Serial.print(' ');
  Serial.println(thermo0_val);
}
