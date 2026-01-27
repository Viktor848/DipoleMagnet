import serial
import sys
sys.path.append('/home/ltp-lab/Desktop/magnet/DipoleMagnet-main/pythonTools')
import DipoleMagnet

portName =''
for port in serial.tools.list_ports.comports():
    #print(port)
    portName = port.device

ard = DipoleMagnet.DipoleMagnet(port = portName)

voltage1 = ard.uv(3)/1000.0
voltage2 = ard.uv(2)/1000.0

amTemp = ard.cels()
rref1 = (1000*voltage1)/(3.3-voltage1)
rref2 = (1000*voltage2)/(3.3-voltage2)
print(rref1)
print(rref2)

while(True):
    voltage1 = ard.uv(3)/1000.0
    resistance = (1000*voltage1)/(3.3-voltage1)
    temp = round(amTemp + (resistance - rref1) / (rref1 * 0.00393), 2)
    print(temp , " degrees Celsius")
    print(ard.cels())
    

# while(True):
#     voltage2 = ard.uv(2)/1000.0
#     resistance = (1000*voltage2)/(3.3-voltage2)
#     temp = 24.5 + (resistance - rref2) / (rref2 * 0.00393)
#     print(temp , " degrees Celsius")
