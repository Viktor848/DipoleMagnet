import time
import serial.tools.list_ports
import sys
sys.path.append('/home/ltp-lab/Desktop/magnet/DipoleMagnet-main/pythonTools')
import DipoleMagnet

portName =''
for port in serial.tools.list_ports.comports():
    print(port.device)
    portName = port.device
ard = DipoleMagnet.DipoleMagnet(port = portName)

while(True):
    time.sleep(1)
    s1calib = (float(ard.dmm(0)) + 5)
    s2calib = (float(ard.dmm(1)) + 13)
    gaphalf = 51
    #print("Sensor 1: ", ard.dmm(0))
    print("Sensor 1: ", s1calib)
    time.sleep(1)
    #print("Sensor 2: ", ard.dmm(1))
    print("Sensor 2: ", s2calib)
    # print("Gap 1: " , (s1calib*0.64))
    # print("Gap 2: " , (s2calib*0.48))
    time.sleep(1)
    leftGap = 51.5-(s1calib-32)
    time.sleep(1)
    rightGap = 51.5-(s2calib-24)
    print("Left:", leftGap)
    print("Right:" , rightGap)
    if(leftGap!=rightGap):
        gapDiff = abs(leftGap - rightGap)
        print("The concentrators are not synchronized by ", gapDiff)
        #continue
    print(leftGap + rightGap)













































































































































































    
