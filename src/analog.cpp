#include <Arduino.h>
#include <ctype.h>
#include "analog.h"
#include <EEPROM.h>


uint8_t adc_range_driver[] = {DEFAULT,INTERNAL1V1, INTERNAL2V56};  // константи с който се сетва ADCto  напроцесора
uint16_t adc_range_volts[3];// = {5000,          1100,         2560}; 
uint8_t hardware_adc_range = 0;

/*
   обхвати: 0, когато се мери спремо захранване околу 5В
           2, когато се мери спямо референс 2.5...В
           1  когато се мери спрямо реф    1.1.. В

   референси -> а/ две неща константа с която да бъде включен
              б/ реална стойност на напрежението му
*/
void init_AnalogImputs_static_vals(void){
    //adc_range_driver[0] = DEFAULT;
    //adc_range_driver[1] = INTERNAL1V1;
    //adc_range_driver[2] = INTERNAL2V56;

    adc_range_volts[0] =   4610; //5000;
    adc_range_volts[1] =   1121; //1100;
    adc_range_volts[2] =   2513; //2560;

}


void ee_save_analog_static_vals(void){
    
     EEPROM.put(EE_VAR_ADDRESS, adc_range_volts);

}


void ee_read_analog_static_vals(void){
    
     EEPROM.get(EE_VAR_ADDRESS, adc_range_volts);

}



AnalogInput::AnalogInput(uint8_t analog_pin){
    _pin = analog_pin; // реалният крак
   
    range = 2;
    //range = 0; //ref.2.5v
    //hardware_adc_range = 0; //обхват на ацп-то

    for(uint8_t i = 0; i < BUFFER_MAX; i++ ){
        last_results[i] = analogRead(_pin);
    }
    last_resupt_pointer =0;

}

void AnalogInput::sample(){
    if(range != hardware_adc_range){
        hardware_adc_range = range;
        analogReference(adc_range_driver[range]);
        delay(15);
        analogRead(_pin);
        delay(5);
        analogRead(_pin);
    }
    last_results[last_resupt_pointer++] = analogRead(_pin);
    if(last_resupt_pointer >= BUFFER_MAX) last_resupt_pointer =0;
}

uint8_t AnalogInput::get_range(){return range;}
void AnalogInput::set_range(uint8_t r){
          if(r>2) r=0;
          range = r;      
     }

uint16_t AnalogInput::read(){
     uint32_t temp_sum=0;
     for(uint8_t i =0 ; i< BUFFER_MAX; i++){
        temp_sum = temp_sum + (uint16_t)last_results[i]; 
     }
    
     return (uint16_t)( temp_sum/((uint32_t)BUFFER_MAX) );
     
}

uint16_t AnalogInput::read_volts(void){
    uint32_t temp_var  =  (uint32_t) read();
    temp_var = temp_var *  (uint32_t) (adc_range_volts[range]);
    temp_var = temp_var/1023;

    return (uint16_t)temp_var;
}

uint16_t AnalogInput::automatic_mesure(void){
   
    set_range(1); 
    for(uint8_t i=0 ; i < BUFFER_MAX; i++){
       sample();
    }
    if(read() > 1015){
        set_range(2);
        for(uint8_t i=0 ; i < BUFFER_MAX; i++){
          sample();
        }
        if(read() > 1015){
            set_range(0);
            for(uint8_t i=0 ; i < BUFFER_MAX; i++){
              sample();
            }
        }

    }

    return  read();      
           
}

uint16_t AnalogInput::automatic_mesure_volts(void){
   
   uint32_t temp_var = automatic_mesure();

    temp_var = temp_var *  (uint32_t) (adc_range_volts[range]);
    temp_var = temp_var/1023;

    return (uint16_t)temp_var;     
  
}