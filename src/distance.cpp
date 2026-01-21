
#include <Arduino.h>
#include "Cmd.h"
#include <Wire.h>
#include <VL6180X.h>
#include "board.h"

VL6180X sensor;


void distance_init(){
 
  // I2C setup
  Wire.begin();
  //Wire.setClock(400000); 
  Wire.setClock(1000);

  
  digitalWrite(DISTANCE_ENABLE_PIN_0, LOW); // Enable the sensor
  digitalWrite(DISTANCE_ENABLE_PIN_1, LOW); // Enable the sensor
  pinMode(DISTANCE_ENABLE_PIN_0, INPUT); // Set the enable pin as output
  pinMode(DISTANCE_ENABLE_PIN_1, OUTPUT); // Set the enable pin as output


  //sensor.init();
  //sensor.configureDefault();
  //sensor.setTimeout(500);

}

uint16_t distance(void){
    sensor.init();
    sensor.configureDefault();
    sensor.setTimeout(500);
    uint16_t sum = 0;
    for(int i = 0; i < 16; i++){
        sum += sensor.readRangeSingleMillimeters();
        if (sensor.timeoutOccurred()) { return 0xFFFF; }
    }
    return sum / 16;
}

void _command_distnce_read(int args_num,char **args){
    Stream *s = cmdGetStream();
    if( args_num > 1){
        uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
        if(tmp_int1 == 1){
            pinMode(DISTANCE_ENABLE_PIN_0, OUTPUT);
            pinMode(DISTANCE_ENABLE_PIN_1, INPUT);
        } 
        else{
            pinMode(DISTANCE_ENABLE_PIN_0, INPUT);
            pinMode(DISTANCE_ENABLE_PIN_1, OUTPUT);
        }
    }
    else{

        pinMode(DISTANCE_ENABLE_PIN_0, INPUT);
        pinMode(DISTANCE_ENABLE_PIN_1, OUTPUT);
    }
    delay(1);
    distance();
    s->print(distance());
    s->println();

    

  }

 void  _command_distance_range(int args_num,char **args){
    Stream *s = cmdGetStream();
    if( args_num > 1){
        uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
        if((tmp_int1 < 1) || (tmp_int1 > 3)){
            tmp_int1 = 1;         
        } 
        sensor.setScaling(tmp_int1); 
    }
    s->println(sensor.getScaling());
    s->println();
  }

  