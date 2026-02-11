#ifndef __ANALOG__H
#define __ANALOG__H
#include <Arduino.h>
#include <ctype.h>
#define BUFFER_MAX 64    // колко стойности да се усредняват (едно и също за всеки канал)
#define EE_VAR_ADDRESS 0 // адрес в ее-прома където се пишат и четат тойностите на реф.волтажа  

void init_AnalogImputs_static_vals(void); // инициализира стойностите на референсите (adc_range_volts[]) 
                                          //със стандартни.
void ee_read_analog_static_vals(void);    // Записва волтажът на референсите (adc_range_volts[]) 
                                          //в постоянната памет ЕЕпром. 
void ee_save_analog_static_vals(void);    // чете стойностите на волтажите на референсите 
                                          //(adc_range_volts[]) от постоянна памет.


extern uint8_t adc_range_driver[];// = {DEFAULT,INTERNAL1V1, INTERNAL2V56}; const сетват ADC-to
extern uint16_t adc_range_volts[];// = {5000,          1100,         2560}; ref.  стойности в mV/



class AnalogInput{

private:
uint8_t _pin;   // analog pin number   
uint8_t range;  // ADC range 0 - 5v, 1 - 1.1V, 2 - 2.5V
uint16_t last_results[BUFFER_MAX];
uint8_t last_resupt_pointer; // last_result_pointer in last_results 
                             // показалец към последният резултат записан в масива last_results 

public:
//static void init_range_constants(void);
AnalogInput(uint8_t);   // параметър крак на налоговият импут
void sample();          // измерва стойност и вкарва в масива за осредняване
void set_range(uint8_t);// сетва обхвата на канала  
uint8_t get_range(void);// връща пбхвата на канала
uint16_t read(void);    // чете в стойностти на ADC-to
uint16_t read_volts(void);//чете преизчислени волти
uint16_t automatic_mesure(void); // мери, като сам си сетва обхвата в стойности на ADC-to
uint16_t automatic_mesure_volts(void); // като горното но преизчислено в волти
};


#endif