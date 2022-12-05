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
    img_count = 1
    Direction = ""
    Angle = 0


class MyController(Controller, Global):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_up_arrow_press(self):
        Global.Direction ="F"
        ArduinoSerial.write(Global.Direction.encode())
       
    def on_down_arrow_press(self):
        Global.Direction ="B"
        ArduinoSerial.write(Global.Direction.encode())

    def on_left_arrow_press(self):
        Global.Direction ="L"
        ArduinoSerial.write(Global.Direction.encode())

    def on_right_arrow_press(self):
        Global.Direction ="R"
        ArduinoSerial.write(Global.Direction.encode())
    
    def on_square_press(self):
        Global.Direction ="S"
        ArduinoSerial.write(Global.Direction.encode())
    
    def on_x_press(self):
        Global.state = 1
            
    def on_circle_press(self):
        Global.state = 0

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

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
    camera = cv2.VideoCapture(0)
    camera.set(3,320)
    camera.set(4,160)
        
    while( camera.isOpened()):
            
            
           

        if Global.state == 1:
            while True:
                    
                if Global.state == 0:
                        
                    break


        _, image = camera.read()
            

        crop_img = image[80:160,0:320]

        gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)

        blur = cv2.GaussianBlur(gray,(5,5),0)

        ret, thresh1 = cv2.threshold(blur,95,255,cv2.THRESH_BINARY)

        save_image = cv2.erode(thresh1, None, iterations=1)
        save_image = cv2.dilate(save_image, None, iterations=3)
        cv2.imshow("save_img", save_image)
        
            
        print(Global.Direction)
        print(Global.img_count)
        if Global.Direction == "F":
            Global.Angle =90
            print(Global.Angle)
            cv2.imwrite("%s_%05d_%03d.png" % (IMGpath,Global.img_count,Global.Angle), save_image)
            Global.img_count = Global.img_count + 1
        elif Global.Direction == "L":
            Global.Angle =45
            cv2.imwrite("%s_%05d_%03d.png" % (IMGpath,Global.img_count,Global.Angle), save_image)
            Global.img_count = Global.img_count + 1
        elif Global.Direction == "R":
            Global.Angle =135
            cv2.imwrite("%s_%05d_%03d.png" % (IMGpath,Global.img_count,Global.Angle), save_image)
            Global.img_count = Global.img_count + 1
           
        print('End')

        # cv2.imwrite("%s_%05d_%03d.png" % (IMGpath,Global.img_count,Global.Angle), save_image)
        # Global.img_count += 1


        cv2.waitKey(300)

        
        if cv2.waitKey(1) == ord( 'q' ):
            break

    cv2.destroyAllWindows()



if __name__ == '__main__':
    
    task1 = threading.Thread(target= Thread_Joystick)
    task2 = threading.Thread(target= Thread_CAM)

    task1.start()
    task2.start()
    


    
