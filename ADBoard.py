import time
import serial
import serial.tools.list_ports
import datetime as dt
import matplotlib.pyplot as plt
from pyqtgraph import plot
# board = serial.Serial('COM4', baudrate=230400)

# nr. masuratoare, frecventa, impedanta, faza, capacitate

def ComportAvailable():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    # print("Connected COM ports: " + str(connected)) #only for test purpose
    return connected

def ADBoardConnect(port, baud):
    ADBoard = serial.Serial(port, baudrate=baud, timeout=1)
    time.sleep(0.1)
    return ADBoard

def ADBoardRead(ADBoard):
    meas = ADBoard.readline()
    meas = meas.decode()
    meas = meas[0:-1]
    time.sleep(0.1)
    return meas

