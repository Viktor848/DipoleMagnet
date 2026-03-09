import serial
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pythonTools'))
import DipoleMagnet
import time

portName =''
for port in serial.tools.list_ports.comports():
    #print(port)
    portName = port.device

ard = DipoleMagnet.DipoleMagnet(port = portName)
ard.all_references(2)
#print(ard.uv(3))
print("start")
voltage1 = ard.uv(3)/1000.0
voltage2 = ard.uv(2)/1000.0
rref1 = (1000*voltage1)/(3.28-voltage1)
# vout = ard.uv(0)*(5.0/1023.0)
# print(vout)
# print(1000*(1/(5/(vout-1))))
# print(5/vout-1)
while(True):
    start = time.time()
    sum1 = 0
    sum2 = 0
    counter = 0
    for i in range(0, 20):
        voltage1 = ard.uv(3)/1000.0
        voltage2 = ard.uv(2)/1000.0
        sum1 += voltage1
        sum2 += voltage2
        counter += 1
        
    avg1 = round((sum1/counter), 6)
    avg2 = round((sum2/counter), 6)
    resistance1 = (1000*avg1)/(3.28-avg1)
    resistance2 = (1000*avg2)/(3.28-avg2)
    end = time.time()
    #print(resistance)
    print(avg1)
    print(avg2)
    print(resistance1)
    print(resistance2)
    print(end-start)

    amTemp = ard.cels()
    temp = round(amTemp + (resistance1 - rref1) / (rref1 * 0.00393), 2)
    print(temp , " degrees Celsius")
    print(amTemp)

# while(True):
#     voltage2 = ard.uv(2)/1000.0
#     resistance = (1000*voltage2)/(3.3-voltage2)
#     temp = 24.5 + (resistance - rref2) / (rref2 * 0.00393)
#     print(temp , " degrees Celsius")
