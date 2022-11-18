import cv2
import numpy as np
import threading
import serial , time
import enum




ArduinoSerial = serial.Serial(port = "/dev/ttyACM0", 
	baudrate= 115200,
	timeout= 1)

blueSerial = serial.Serial(port="/dev/rfcomm0",baudrate=115200,timeout=0.1)

CarState = ""
sdata = ""
filepath ="/home/pi/project/Finalproject/Track_Img/"


def Thread_Arduino():
    global CarState
    while True:
        if ArduinoSerial.in_waiting > 0:
            
            
            ArduinoSerial.write(CarState.encode())
            ArduinoSerial.flush()

def Thread_Joystick():
    global sdata
    while True:
        if blueSerial.in_waiting >0:
        
            data = blueSerial.readline()
            ArduinoSerial.write(data)
            sdata = data.decode('utf-8').rstrip()

         
        

def Thread_CAM():
    i = 0
    global CarState
    global sdata
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while( camera.isOpened()):
        
        if sdata == 'PAUSE':
            while True:
                if sdata == 'START':
                    break
        
       

        
        _, image = camera.read()
        

        crop_img = image[60:120,0:160]

        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray,(5,5),0)

        ret, thresh1 = cv2.threshold(blur,130,255,cv2.THRESH_BINARY)

        save_image = cv2.erode(thresh1, None, iterations=2)
        save_image = cv2.dilate(save_image, None, iterations=2)
        cv2.imshow('save_image',save_image)

        cv2.imwrite("%s_%05d.png" % (filepath,i), save_image)
        i = i + 1

        time.sleep(0.1)

        contours,hierarchy = cv2.findContours(save_image.copy(),1,cv2.CHAIN_APPROX_NONE)
     
        if cv2.waitKey(1) == ord( 'q' ):
            break

    cv2.destroyAllWindows()



if __name__ == '__main__':
    
    task1 = threading.Thread(target= Thread_Arduino)
    task2 = threading.Thread(target= Thread_Joystick)
    task3 = threading.Thread(target= Thread_CAM)
    task1.start()
    task2.start()
    task3.start()
    


    
