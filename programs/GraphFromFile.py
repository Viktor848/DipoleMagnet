import csv
import matplotlib.pyplot as plt

dataSensor1 = []
dataSensor2 = []
with open("/home/ltp-lab/Desktop/magnet/pythonn-main/data.csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
                print(row)
                if row[1] == 'Sensor 1:':
                    dataSensor1.append(float(row[2]))
                else:
                    dataSensor2.append(float(row[2]))
# for data in dataSensor1:
#         print(data)

plt.plot(dataSensor1, label='Sensor 1', color='blue')
plt.plot(dataSensor2, label='Sensor 2', color='red')

# Add labels and legend
plt.ylabel('Ampers')
plt.legend()

plt.show()