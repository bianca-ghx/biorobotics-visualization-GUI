import serial

ser = serial.Serial("COM8", 9600)

# Wait for the arduino to setup
# the serial communication.
connected = False
while not connected:
	serin = ser.read()
	connected = True

i = 0
while True:
    # if i == 0:
    #     ser.write(b"95")	# Send the value to arduino
    #     i+=1
    serial_b = ser.readline()
    string_n = serial_b.decode()
    string = string_n.rstrip()
    print(string)

