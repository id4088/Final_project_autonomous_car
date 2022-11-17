import serial
import time

ser = serial.Serial(port = "/dev/ttyACM1", 
	baudrate= 115200,
	timeout= 1)

f = "Forward_100"

if __name__ == '__main__':
	while True:
		if ser.in_waiting > 0:
			ser.write(f.encode())
			line = ser.readline().decode('utf-8').rstrip()
			print(line)
			ser.flush()
		
