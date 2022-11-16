import serial

if __name__ == '__main__':
    com = serial.Serial(port = "/dev/ttyACM0",
		baudrate = 9600,
		bytesize = serial.EIGHTBITS,
		parity = serial.PARITY_NONE,
		timeout = 1)
    
    s = "hello"
    
    
    while True:
        if com.in_waiting > 0:
            com.write(s.encode())
            line = com.readline().decode('utf-8').rstrip()
            print(line)
            com.flush()
            
    
