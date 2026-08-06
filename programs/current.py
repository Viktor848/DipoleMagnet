import serial
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pythonTools'))
import DipoleMagnet

portName =''
for port in serial.tools.list_ports.comports():
    print(port)
    portName = port.device

ard = DipoleMagnet.DipoleMagnet(port = portName)
while True:
    print(ard.uv(0))
    print(ard.uv(1))
    print('Sensor 1: ', ard.aread(0, "ampers"))
    print('Sensor 2: ', ard.aread(1, "ampers"))
    
    time.sleep(1)