import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial.tools.list_ports
import csv
import datetime
import sys
sys.path.append('/home/ltp-lab/Desktop/magnet/DipoleMagnet-main/pythonTools')
import DipoleMagnet

portName =''
for port in serial.tools.list_ports.comports():
    #print(port)
    portName = port.device

def animate(i, dataList1, dataList2, ard):
    #timestamp = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    arduinoData_string1 = ard.aread(0, 'ampers')
    arduinoData_string2 = ard.aread(1, 'ampers')
    # try:
    arduinoData_float1 = round(float(arduinoData_string1), 2)
    arduinoData_float2 = round(float(arduinoData_string2), 2)
    dataList1.append(arduinoData_float1)
    dataList2.append(arduinoData_float2)

    # with open("data.csv", "a", newline="") as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow([timestamp, 'Sensor 1:', arduinoData_float1,'ampers'])
    #     writer.writerow([timestamp, 'Sensor 2:', arduinoData_float2,'ampers'])

    # except:
    #     pass

    del dataList1[:-50]  # Изтриване на по-старите елементи, запазва само последните 50
    del dataList2[:-50]

    ax.clear()
    ax.plot(dataList1, label='Sensor 1', color='blue')
    ax.plot(dataList2, label='Sensor 2', color='red')
    ax.legend()

    #ax.set_ylim([-(arduinoData_float1+0.5), arduinoData_float1+0.5])
    ax.set_ylim([-1, 1])

    ax.set_title("Arduino Data")
    ax.set_ylabel("Value")

    for x in range(len(dataList1)):
        print('Sensor 1: ', dataList1[x])
        print('Sensor 2: ', dataList2[x])
                           # Set title of y axis 

dataList1 = []                                           # Create empty list variable for later use
dataList2 = []

fig = plt.figure()                                      # Create Matplotlib plots fig is the 'higher level' plot window

ax = fig.add_subplot(111)                               # Add subplot to main fig window

ard = DipoleMagnet.DipoleMagnet(port = portName)
time.sleep(2)                                           # Time delay for Arduino Serial initialization 

                                                        # Matplotlib Animation Fuction that takes takes care of real time plot.
                                                        # Note that 'fargs' parameter is where we pass in our dataList and Serial object. 
ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(dataList1, dataList2, ard), interval=100) 
plt.style.use('_mpl-gallery')
plt.show()                                              # Keep Matplotlib plot persistent on screen until it is closed       


 