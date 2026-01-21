#include <Arduino.h>
#include "Ticker.h" 
#include "board.h"
#include "tasks.h"
#include "analog.h"
//#include "Cmd.h"
//#include "commands.h"

void led_task(void);
void analog_task(void);

Ticker ledTicker(led_task, LED_PERIOD, 0, MILLIS);
Ticker analogTicker(analog_task,ANALOG_PERIOD, 0, MILLIS);

//=====================================================


void analog_task(){
  static uint8_t cannel_number = 0;
  apins[cannel_number].sample(); 
  if(++cannel_number >= APIN_MAX) cannel_number=0; 
}



uint8_t blink_number = 0;
void led_blinks(uint8_t i){
  blink_number = i; 
}


void led_task(void){
  static uint8_t temp_led_state = 0;
  if(temp_led_state){
      if((temp_led_state%2 == 0) &&  (temp_led_state > 2* blink_number)){
        digitalWrite(LED, HIGH);
      }
      else{
        digitalWrite(LED, LOW);
      }
      temp_led_state--; 
  }
  else{
       temp_led_state = 4 * blink_number; 
  }
}


void tasks_setup(){
    
    pinMode(LED, OUTPUT);
    digitalWrite(LED,LOW);
    ledTicker.start();
    led_blinks(mode+1);
    analogTicker.start();
}

void tasks_loop(){
    analogTicker.update();
    analogTicker.update();
    ledTicker.update();
}

