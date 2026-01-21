// ---  Serial commands ...

/*
format:
      command param1 param2 ...
      param1 = the channel number (without = all)
      param2 = parameter to be set (without = to read this parameter) 
      ----------------------------------------------------------------
      
      
      hello 
      returns-> strings name of this project and processor type
      
      ---
      args - test function
      
      ---
      mode param1 - led blinks parram1
      return -> recent mode

      ---
      tstval - test function
      
      ---
      aur param1 
      reads automatic(sets range automatic) raw(ADC value) of the param1 channel 
      -> setted the best range for the channel and the raw ADC value in bits

      ---
      auv param1 - automatic(finds the range)  value of the param1 channel  
      returns-> voltage in mVolsts
      
      ---
      rng param1 param2 - manual sets range ot the param1 channel with param2(could be 0,1,2) 
      returrns -> recent range 
      
      ---
      ur param1 
      returns ->range and ADC value of the param1 channel
      
      ---
      uv param1 
      returns ->voltage in mV of param1 channel
      
      ---
      setcalib param1 param2 sets voltage refference
      param1 0,1,2 - which refference. 1023 bits are param2 mV 
      
      ---
      calibtoee  saves in ee all values for 0,1,2 renges
      
      ---
      calibfromee - restore calibration from ee
  */



// ---  Cmd Callbacks
#include <Arduino.h>
#include "Cmd.h"
#include "commands.h"
#include "analog.h"
#include "board.h"
#include "tasks.h"
#include "distance.h"



void _ee_read_analog_static_vals(int args_num,char **args){
  ee_read_analog_static_vals();
}

void _ee_save_analog_static_vals(int args_num,char **args){
  ee_save_analog_static_vals();
}


void _set_calib_vals(int args_num,char **args){
  Stream *s = cmdGetStream();
  if( args_num > 1){
    uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
    if(tmp_int1 < 3){
      uint16_t tmp_int2 = cmdStr2Num(args[2], 10);
      if(tmp_int2 < 5000){
        adc_range_volts[tmp_int1] = tmp_int2;
      }
      s->println( adc_range_volts[tmp_int1]);
    return;
    } 
  }
  
  for ( uint8_t tmp_int1= 0;  tmp_int1< 3; tmp_int1++){
      s->print( adc_range_volts[tmp_int1]);
      if(tmp_int1 < 2)s->print(",");
  }
  s->println();

}



void _read_raw(int args_num,char **args){
  Stream *s = cmdGetStream();
  if( args_num > 1){
    uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
    if(tmp_int1 < APIN_MAX){
      s->print( apins[tmp_int1].get_range());
      s->print(",");
      s->println( apins[tmp_int1].read());
      s->println();
    return;
    } 
  }
  
  for ( uint8_t tmp_int1= 0;  tmp_int1< APIN_MAX; tmp_int1++){
      s->print( apins[tmp_int1].get_range());
      s->print(",");
      s->print( apins[tmp_int1].read());
      s->println();
  }
  s->println();
}

void _read_volts(int args_num,char **args){
  Stream *s = cmdGetStream();
  if( args_num > 1){
    uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
    if(tmp_int1 < APIN_MAX){
      //s->print( apins[tmp_int1].get_range());
      //s->print("  ");
      s->println( apins[tmp_int1].read_volts());
    return;
    } 
  }
  
  for ( uint8_t tmp_int1= 0;  tmp_int1< APIN_MAX; tmp_int1++){
      //s->print( apins[tmp_int1].get_range());
      //s->print("  ");
      s->print( apins[tmp_int1].read_volts());
        if(tmp_int1< (APIN_MAX-1))s->print(",");
  }
  s->println();
}

void _analog_set_range(int args_num,char **args){
  Stream *s = cmdGetStream();
  if( args_num > 1){
    uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
    if(tmp_int1 < APIN_MAX){
      uint8_t tmp_int2 = cmdStr2Num(args[2], 10);
      if(tmp_int2 < 3){
        apins[tmp_int1].set_range(tmp_int2);
      }
      s->println( apins[tmp_int1].get_range());
    return;
    } 
  }
  
  for ( uint8_t tmp_int1= 0;  tmp_int1< APIN_MAX; tmp_int1++){
      s->print( apins[tmp_int1].get_range());
      if(tmp_int1< (APIN_MAX-1))s->print(",");
      
  }
  s->println();

}





void _auto_read_volts(int args_num,char **args){
  Stream *s = cmdGetStream();
  if( args_num > 1){
    uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
    if(tmp_int1 < APIN_MAX){
      //s->print( apins[tmp_int1].get_range());
      //s->print("  ");
      s->println( apins[tmp_int1].automatic_mesure_volts());
    return;
    } 
  }
  
  for ( uint8_t tmp_int1= 0;  tmp_int1< APIN_MAX; tmp_int1++){
      //s->print( apins[tmp_int1].get_range());
      s->print( apins[tmp_int1].automatic_mesure_volts());
      if(tmp_int1 < (APIN_MAX -1)) s->print(",");
  }
  s->println();

}


void _auto_read_raw(int args_num,char **args){
  Stream *s = cmdGetStream();
  if( args_num > 1){
    uint8_t tmp_int1 = cmdStr2Num(args[1], 10);
    if(tmp_int1 < APIN_MAX){
      s->print( apins[tmp_int1].get_range());
      s->print(",");
      s->println( apins[tmp_int1].automatic_mesure());
      s->println();
    return;
    } 
  }
  
  for ( uint8_t tmp_int1= 0;  tmp_int1< APIN_MAX; tmp_int1++){
      s->print( apins[tmp_int1].get_range());
      s->print(",");
      s->print( apins[tmp_int1].automatic_mesure());
      s->println();

  }
  s->println();
  
}


//  
float test_val;

void _tst_val(int arg_cnt, char **args){
  Stream *s = cmdGetStream();
  if (arg_cnt > 1)
    test_val = reg(--arg_cnt, ++args);

  s->println( test_val);
}



void add_commands(void)
{
  
  //add("serial_command", pointer to function);
  
  cmdAdd("args", _args);               // test cmd
  cmdAdd("tstval", _tst_val);          // test cmd
  cmdAdd("hello",_hello);              // serial return strings with name and processor
  cmdAdd("mode", _mode);               // test cmd
  cmdAdd("dmm",_command_distnce_read); // distance sensor 
  cmdAdd("drng", _command_distance_range);
  cmdAdd("aur", _auto_read_raw);
  cmdAdd("auv", _auto_read_volts);
 
  cmdAdd("ur", _read_raw);
  cmdAdd("uv", _read_volts);
   cmdAdd("aref", _analog_set_range);  // which ref is used
  cmdAdd("vref",  _set_calib_vals);    // voltage of the internal ref
  cmdAdd("calibtoee",_ee_save_analog_static_vals);
  cmdAdd("calibfromee", _ee_read_analog_static_vals);
}



void _args(int arg_cnt, char **args)
{
  Stream *s = cmdGetStream();
  s->println(arg_cnt);
  for (int i = 0; i < arg_cnt; i++)
    s->println(args[i]);
}

void _hello(int arg_cnt, char **args)
{
  Stream *s = cmdGetStream();
  s->println(__NAME);
  s->println("atmega2560");
  s->println();
}

void _mode(int arg_cnt, char **args)
{
  Stream *s = cmdGetStream();
  if (arg_cnt > 1)
    mode = (int)reg(--arg_cnt, ++args);

  if(mode > MAX_MODE) mode = MAX_MODE;
  else if (mode < MIN_MODE) mode = MIN_MODE;
  led_blinks(mode+1);
  s->println(mode);
}



float reg(int cnt, char **arg)
{
  //Stream *s = cmdGetStream();
  int sign = +1;
  int tmp_int1, tmp_int2;
  float tmp;

  if (cnt == 1)
  {
    tmp_int1 = cmdStr2Num(arg[0], 10);
    tmp = (float)tmp_int1;
  }
  else if (cnt >= 2)
  {
    switch (arg[1][0])
    {
    case 'H':
    case 'h':
    case 'X':
    case 'x':
      tmp_int2 = cmdStr2Num(arg[0], 16);
      tmp = (float)tmp_int2;
      break;

    default:

      int power1 = cmdStr2Num(arg[1], 10);
      int num1 = cmdStr2Num(arg[0], 10);
      float power = (float)power1;
      float num = (float)num1;
      tmp = (num * pow(10.0, (sign * power)));
      // s->print(tmp); s->print("  ");
    }
  }
  return tmp;
}
