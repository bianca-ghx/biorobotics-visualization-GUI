#include <Wire.h>
#include "Adafruit_VL6180X.h"
#include "HX711.h"

const int DOUT=A1;
const int CLK=A0;

HX711 balanza;

Adafruit_VL6180X vl = Adafruit_VL6180X();

const int pin = 6;
int option;
int i;
int j;
int Setpoint;

void setup() {
  Serial.begin(9600);
  pinMode(pin, OUTPUT);
  pinMode(3, OUTPUT);

  while (!Serial) {
    delay(1);
  }

  Serial.println("Adafruit VL6180x test!");
  if (! vl.begin()) {
    Serial.println("Failed to find sensor");
    while (1);
  }
  Serial.println("Sensor found!");
  
  balanza.begin(DOUT, CLK);
  Serial.print("Lectura del valor del ADC:  ");
  Serial.println(balanza.read());
  Serial.println("No ponga ningun  objeto sobre la balanza");
  Serial.println("Destarando...");
  Serial.println("...");
  balanza.set_scale(128275); // Establecemos la escala
  balanza.tare(20);  //El peso actual es considerado Tara.
}

void loop() {

  Serial.print("Peso: ");
  Serial.print(balanza.get_units(20),3);
  Serial.println(" kg");
  delay(10);
  
  float lux = vl.readLux(VL6180X_ALS_GAIN_5);

  //Serial.print("Lux: "); Serial.println(lux);

  uint8_t range = vl.readRange() + 10 - 54;
  uint8_t status = vl.readRangeStatus();

  if (status == VL6180X_ERROR_NONE) {
    Serial.print("Range: "); Serial.println(range);
  }

  if (Serial.available()) {
    int distancia = Serial.parseInt();

    while (distancia == 0) {
      distancia = Serial.parseInt();
      range = vl.readRange() + 10 - 54;
      Serial.print("Range: "); Serial.println(range);

       //Serial.print("Peso: ");
      Serial.print(balanza.get_units(20),3);
      Serial.println("");
      //Serial.println(" kg");
    }
    
    Serial.print("Distancia introducida = ");
    Serial.println(distancia);

    for (j = 0; j < 4; j++) {
      //if(range > 250){
      //  range = -range;
      //}
      while (distancia > range - 2) {
        analogWrite(pin, 255);
        digitalWrite(3, HIGH);   // poner el Pin en HIGH
        delay(5);               // esperar un segundo
        digitalWrite(3, LOW);    // poner el Pin en LOW
        //delay(10);               // esperar un segundo
        range = vl.readRange() + 10 - 55;
        //Serial.print("Range: "); Serial.println(range);
        //if(range > 250){
        //  range = -range;
        //}

         Serial.print("Peso: ");
         Serial.print(balanza.get_units(1),3);
         Serial.println("");
         //Serial.println(" kg");
      }
      while (distancia < range + 2) {
        analogWrite(pin, 0);
        digitalWrite(3, HIGH);   // poner el Pin en HIGH
        delay(5);               // esperar un segundo
        digitalWrite(3, LOW);    // poner el Pin en LOW
        //delay(10);               // esperar un segundo
        range = vl.readRange() + 10 - 53;
        //Serial.print("Range: "); Serial.println(range);
        //if(range > 250){
        //  range = -range;
        //}

         Serial.print("Peso: ");
         Serial.print(balanza.get_units(1),3);
         Serial.println("");
         //Serial.println(" kg");
      }
    }        
  }
}
