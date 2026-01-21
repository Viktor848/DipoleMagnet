/*


v1.2 12.11.2024
---------------------------
Тук се въщаме отново на serial 9600

Команда rng e променена на vref
още setvref, no остават calibtoee, calibfromee


v1.1 06.11.24 
---------------------------
Променям принта с запетайки за да стигна до формата на pykiba

V01 30.10.2024  

  --- KrustioMag ---
  processor: ATMega2560
  serila interface: monitor_speed = 115200  
  
  Проектът е инспириран от магнит/криостат на Кръстьо
  Превръща Arduino Mega в цифров волтметър.

  Напреженията по аналоговите входовете на Arduinoto се сравняват 
  с два вътрешни референса,или с захранващо напрежение разделени на 1023 . 
  Референсите се менят от температура или на различните процесори. 

Софтуера може да изпълнява команди получени през серийният порт. Има команди за:

- да получава нови референтни стойности за опорните напрежения.
- да записва реф. Стойности в постоянна памет и да ги чете от там.
- да чете сурови стойности на различни крака(канали) с въможност да се свързват ADC-t0 на процесора.
- да пресмята реално напрежение в mV през стойността на референса.
- усредняване от няколко измервания.

файлове:

main.cpp - Това! Сглобяване на всичко...
analog.h - малка надстройна на функциите за четене на аналогови входове
commands.cpp - дифинирани всиччки команди изпълнявани през серииният канал
tasks.cpp - дефинирани два периодични процеса свързани към таймери 
а/ мигане на светодиода, 
б/ усредняване на аналоговият сигнал


*/




#include <Arduino.h>


#include "board.h"
#include "tasks.h"

#include "Cmd.h"
#include "commands.h"
#include "analog.h"
#include "distance.h"
#include "temperature.h"



 
/*
- mm - > dmm, rng -> drng //
- краката влючени в масива са каналите на волтметъра
- подредбата в масива дефинира номера на канала на волтметъра
/в случая подредбата съвпада с номера на крака/
*/
AnalogInput apins[] = {AnalogInput(A0),   //An array with all used analog pins
                       AnalogInput(A1), 
                       AnalogInput(A2), 
                       AnalogInput(A3)}; 

// Global control variable -->  не се ползва
uint8_t mode = MIN_MODE; 

void setup() {
  distance_init();
  init_AnalogImputs_static_vals(); // -> analog.cpp 
  Serial.begin(9600); // Default monistor_speeed = 9600
  //Serial.begin(115200); // In platformio.ini must be included 
                        //included:" monitor_speed = 115200 " in platformio.ini
  tasks_setup();        // All tasks setup - > tasks.cpp 
  cmdInit(&Serial);     // Init Cmd library with a stream address
  add_commands();       // Adds commands to Cmd -> commands.cpp  
  setup_temperature();
}

// 


void loop() {
 tasks_loop();
 cmdPoll();           // 
}
