import serial
import sys
sys.path.append('/home/ltp-lab/Desktop/magnet/krastioMag-main/pythonTools')
import krastioMag
import time

portName =''
for port in serial.tools.list_ports.comports():
    #print(port)
    portName = port.device

ard = krastioMag.krastioMag(port = portName)
ard.all_references(2)
#print(ard.uv(3))

# vout = ard.uv(0)*(5.0/1023.0)
# print(vout)
# print(1000*(1/(5/(vout-1))))
# print(5/vout-1)
while(True):
    sum1 = 0
    sum2 = 0
    counter = 0
    for i in range(0, 100):
        voltage1 = ard.uv(3)/1000.0
        voltage2 = ard.uv(2)/1000.0
        sum1 += voltage1
        sum2 += voltage2
        counter += 1
    avg1 = round((sum1/counter), 2)
    avg2 = round((sum2/counter), 2)
    print()
    #resistance = ((3.3-voltage1)*1000)/voltage1
    resistance1 = (1000*avg1)/(3.26-avg1)
    resistance2 = (1000*avg2)/(3.26-avg2)

    #print(resistance)
    print(avg1)
    print(avg2)
    print(resistance1)
    print(resistance2)