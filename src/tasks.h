#ifndef _TASKS_H
#define _TASKS_H

#define LED_PERIOD  200 //mS

// 1000 mS / (4 Analog Chanels * 16 samples per S) = 15ms
#define ANALOG_PERIOD 15


void tasks_setup(void);
void tasks_loop(void);
void led_blinks(uint8_t );


#endif