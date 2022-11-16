import cv2
import numpy as np
import threading
import serial

com = serial.Serial(port= "/dev/ttyACM0", baudrate=9600, bytesize= serial.EIGHTBITS, parity= serial.PARITY_NONE, timeout= 1)

s = "hello"

def thread1():
    while True:
        if com.in_waiting > 0:
            com.write(s.encode())
            line = com.readline().decode('utf-8').rstrip()
            print(line)
            com.flush()

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,640)
    camera.set(4,480)
        
    while( camera.isOpened()):
        _, image = camera.read()
        cv2.imshow('camera test',image)
            
        if cv2.waitKey(1) == ord( 'q' ):
            break
            
    cv2.destroyAllWindows()

if __name__ == '__main__':
    task1 = threading.Thread(target= thread1)
    task1.start()
    main()
    
