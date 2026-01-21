#ifndef __BOARD_H
#define __BOARD_H

#define __NAME "Krastiomag"
#include <Arduino.h>

// analogReference()
//DEFAULT: the default analog reference of 5 volts (on 5V Arduino boards) or 3.3 volts (on 3.3V Arduino boards)
//INTERNAL: a built-in reference, equal to 1.1 volts on the ATmega168 or ATmega328P and 2.56 volts on the ATmega32U4 and ATmega8 (not available on the Arduino Mega)
//INTERNAL1V1: a built-in 1.1V reference (Arduino Mega only)
//INTERNAL2V56: a built-in 2.56V reference (Arduino Mega only)
//EXTERNAL: the voltage applied to the AREF pin (0 to 5V only) is used as the reference.

//analogRead()
//Mega2560, 5 Volts, A0 to A14, 10 bits



// EEPROM Atmega2560 (Arduino Mega 2560) 	4096 Bytes


// --- Pins Deffinitions 

#define LED       LED_BUILTIN
#define APIN_MAX  4
/*
in main.cpp
AnalogInput apins[] = {AnalogInput(A0), 
                       AnalogInput(A1), 
                       AnalogInput(A2), 
                       AnalogInput(A3)}; 
*/
extern class AnalogInput apins[];


#define DISTANCE_ENABLE_PIN_0 8
#define DISTANCE_ENABLE_PIN_1 10
// SDA    20
// SCL    21


// --- Operation modes
#define MIN_MODE 0
#define MAX_MODE 3

extern uint8_t mode;

#endif