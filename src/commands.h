#ifndef __COMMANDS_H
#define __COMMANDS_H


void add_commands(void);               // добавя всичките дефиниран команди в сетъпа на итерпретатора
                                       // в commands.cpp описание на следващото 
void _hello(int , char **);
void _args(int arg_cnt, char **args);
void _mode(int arg_cnt, char **args);
float reg(int cnt, char **arg);    // помощна фукция

#endif