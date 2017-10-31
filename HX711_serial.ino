#include <Q2HX711.h>

const byte hx711_data_pin = 10;
const byte hx711_clock_pin = 11;
Q2HX711 hx711(hx711_data_pin, hx711_clock_pin);

void setup() {
  Serial.begin(57600);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  digitalWrite(4, HIGH);
  digitalWrite(5, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);
}

void loop() {
 if (digitalRead(8) == LOW) {
   digitalWrite(4, LOW);
   delay(100);
   digitalWrite(4, HIGH);
   delay(100);
    digitalWrite(5, LOW);
   delay(100);
   digitalWrite(5, HIGH);
   delay(100);
    digitalWrite(6, LOW);
   delay(100);
   digitalWrite(6, HIGH);
   delay(100);
    digitalWrite(7, LOW);
   delay(100);
   digitalWrite(7, HIGH);
   delay(100);
   }
 if (digitalRead(9) == LOW) {
   Serial.println(hx711.read()/8.75 - 981620);
  }
}
