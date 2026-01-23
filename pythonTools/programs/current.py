import serial
import time
import sys
sys.path.append('/home/ltp-lab/oldKM/krastioMag-main(1) (2)/krastioMag-main/pythonTools')
import krastioMag

portName =''
for port in serial.tools.list_ports.comports():
    print(port)
    portName = port.device

ard = krastioMag.krastioMag(port = portName)
while True:
    print(ard.uv(0))
    print(ard.uv(1))
    print('Sensor 1: ', ard.aread(0, "ampers"))
    print('Sensor 2: ', ard.aread(1, "ampers"))
    
    time.sleep(1)