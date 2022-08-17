import time
import serial
import serial.tools.list_ports

def ComportAvailable():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    return connected

def MotorConnect(port, baud):
    arduino = serial.Serial(port, baudrate=baud)
    time.sleep(0.1)
    return arduino

def MotorRead(arduino):
    ser_meas = arduino.readline()
    string_n = ser_meas.decode()
    measurement = string_n
    t = time.time()
    return measurement, t
