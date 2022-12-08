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
IMGpath ="/home/pi/project/Finalproject/Track_auto_Img/"

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
        camera.set(4,160)
        
        while( camera.isOpened()):
            
            
           

            # if Global.state == 1:
            #     while True:
                    
            #         if Global.state == 0:
            #             break


            _, image = camera.read()
            

            #crop_img = image[80:160,0:320]

            save_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            save_image = cv2.GaussianBlur(save_image,(5,5),0)

            ret, thresh1 = cv2.threshold(save_image,95,255,cv2.THRESH_BINARY)

            save_image = cv2.erode(thresh1, None, iterations=1)
            save_image = cv2.dilate(save_image, None, iterations=3)
            cv2.imshow("save_img", save_image)
            
            cv2.imwrite("%s_%05d.png" % (IMGpath,i), save_image)
            i = i + 1

            cv2.waitKey(100)

            contours,hierarchy = cv2.findContours(save_image.copy(),1,cv2.CHAIN_APPROX_NONE)

            if len(contours)>0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])

                print(cx)

                if cx>=80 and cx<= 130:
                    ArduinoSerial.write("L".encode())
                        
                elif (cx>=30 and cx<=65) or (cx>=160 and cx<=210):
                    ArduinoSerial.write("R".encode())
                        
                else:
                    ArduinoSerial.write("F".encode())
        
    
        cv2.destroyAllWindows()



if __name__ == '__main__':
    
    task1 = threading.Thread(target= Thread_RC.Thread_Joystick)
    task2 = threading.Thread(target= Thread_RC.Thread_CAM)

    # task1.start()
    task2.start()
    


    
