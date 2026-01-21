#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "Cmd.h"

#define ONE_WIRE_BUS 5

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

void _get_temperature(int argc, char **args){
   Stream *s = cmdGetStream();
   sensors.requestTemperatures();
   s->println(sensors.getTempCByIndex(0));
   s->println(); 
}

void setup_temperature(void){
    sensors.begin();
    cmdAdd("cels", _get_temperature);
}

