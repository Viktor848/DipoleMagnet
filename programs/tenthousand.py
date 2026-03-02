import serial
import sys
sys.path.append('/home/ltp-lab/DipoleMagnet/pythonTools')
import DipoleMagnet
import time
import pandas as pd

portName =''
for port in serial.tools.list_ports.comports():
    portName = port.device

ard = DipoleMagnet.DipoleMagnet(port = portName)
ard.all_references(2)
print("start")
voltage1 = ard.uv(3)/1000.0
voltage2 = ard.uv(2)/1000.0
rref1 = (1000*voltage1)/(3.28-voltage1)
table = pd.DataFrame(columns=['Time', 'Temperature'])
start = time.time()
while(True):
    
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
    if(end-start>=10000.0):
        break
    amTemp = ard.cels()
    temp = round(amTemp + (resistance1 - rref1) / (rref1 * 0.00393), 2)
    print(temp , " degrees Celsius")
    print(amTemp)
    table.append([end, temp], ignore_index=True)

table.to_csv("Measurements.csv", index=False) 



