import time
import serial
import serial.tools.list_ports

def ComportAvailable():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    return connected

def dSensorConnect(port, baud):
    arduino = serial.Serial(port, baudrate=baud, timeout=1)
    time.sleep(0.1)
    return arduino

def dSensRead(arduino):
    distance = arduino.readline()
    distance = ''.join(c for c in str(distance) if c.isdigit() or c == '.')
    # t = dt.datetime.now().strftime("%H:%M:%S.%f")
    t = time.time()
    time.sleep(0.1)
    return distance, t
