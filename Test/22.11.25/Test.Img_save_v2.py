import cv2
import numpy as np
import threading
import serial , time
import enum
import os
from pyPS4Controller.controller import Controller

      
ArduinoSerial = serial.Serial(port = "/dev/ttyACM0", 
	baudrate= 115200,
	timeout= 1)

BTpath = ""



strdata = "on_x_press"
IMGpath ="/home/pi/project/Finalproject/Track_Img/"

class Global(object):
    state = 1


class MyController(Controller, Global):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_up_arrow_press(self):
        ArduinoSerial.write("F".encode())

    def on_down_arrow_press(self):
        ArduinoSerial.write("B".encode())

    def on_left_arrow_press(self):
        ArduinoSerial.write("L".encode())

    def on_right_arrow_press(self):
        ArduinoSerial.write("R".encode())
    
    def on_square_press(self):
        ArduinoSerial.write("S".encode())
    
    def on_x_press(self):
        Global.state = 1
            
    def on_circle_press(self):
        Global.state = 0

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

class Thread_RC(Global):
    

    def Thread_Joystick():
        global strdata
        global BTpath

        controller.listen()

        while True:
                
            controller.on_up_arrow_press()

            controller.on_down_arrow_press()
                
            controller.on_left_arrow_press()

            controller.on_right_arrow_press()
            
            
            

    def Thread_CAM():
        i = 0
        camera = cv2.VideoCapture(0)
        camera.set(3,320)
        camera.set(4,200)
        
        while( camera.isOpened()):
            
            
           

            if Global.state == 1:
                while True:
                    
                    if Global.state == 0:
                        break


            _, image = camera.read()
            

            crop_img = image[100:200,0:320]

            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray,(5,5),0)

            ret, thresh1 = cv2.threshold(blur,130,255,cv2.THRESH_BINARY)

            save_image = cv2.erode(thresh1, None, iterations=2)
            save_image = cv2.dilate(save_image, None, iterations=2)
            cv2.imshow("save_img", save_image)
            
            cv2.imwrite("%s_%05d.png" % (IMGpath,i), save_image)
            i = i + 1

            cv2.waitKey(100)

            contours,hierarchy = cv2.findContours(save_image.copy(),1,cv2.CHAIN_APPROX_NONE)
        
            if cv2.waitKey(1) == ord( 'q' ):
                break

        cv2.destroyAllWindows()



if __name__ == '__main__':
    
    task1 = threading.Thread(target= Thread_RC.Thread_Joystick)
    task2 = threading.Thread(target= Thread_RC.Thread_CAM)

    task1.start()
    task2.start()
    


    
