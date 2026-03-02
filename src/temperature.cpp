#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "Cmd.h"

//#define ONE_WIRE_BUS 3
// int ONE_WIRE_BUS = 3;
// // Setup a oneWire instance to communicate with any OneWire devices
// OneWire oneWire(ONE_WIRE_BUS);

// // Pass our oneWire reference to Dallas Temperature sensor 
// DallasTemperature sensors(&oneWire);

void _get_temperature(int argc, char **args){
   Stream *s = cmdGetStream();
   int ONE_WIRE_BUS = 3;
    if(argc > 1){
        uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
        ONE_WIRE_BUS = tmp_int1;
    }
   OneWire oneWire(ONE_WIRE_BUS);
   DallasTemperature sensors(&oneWire);
   sensors.begin();
   sensors.requestTemperatures();
   s->println(sensors.getTempCByIndex(0));
   s->println(); 
}

void setup_temperature(void){
    cmdAdd("cels", _get_temperature);
}

