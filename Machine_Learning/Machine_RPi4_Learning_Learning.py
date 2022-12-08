import cv2
import numpy as np
import threading
import serial 
import tensorflow as rf
from tensorflow.keras.models import load_model
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
        
    model_path ='/home/pi/project/Finalproject/machineLearning/model/lane_navigation_final.h5'
    model = load_model(model_path)
    while( camera.isOpened()):
            
            
           

        if Global.state == 1:
            while True:
                    
                if Global.state == 0:
                        
                    break


        _, image = camera.read()
            
        # cv2.imshow('Original',image)

        height,_,ch =image.shape
        image=image[int(height/2):,:,:]
        print(ch)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        processed_image = cv2.GaussianBlur(gray,(5,5),0)

        ret, thresh1 = cv2.threshold(processed_image,95,255,cv2.THRESH_BINARY)

        # processed_image = cv2.erode(thresh1, None, iterations=1)
        # processed_image = cv2.dilate(processed_image, None, iterations=3)

        cv2.imshow("pre", processed_image)

        processed_image = cv2.resize(processed_image,(80,320))
        
        
        processed_image=processed_image / 255
        # processed_image = np.expand_dims(processed_image, axis=-1)
        # processed_image = processed_image.reshape([-1,80,320,3])
        

        X =np.asarray([processed_image])
        steering_angle = int(model.predict(X)[0])
        # print("predict angle:",steering_angle)

        print(Global.Direction)
        print(Global.img_count)
        if Global.Direction == "F":
            if steering_angle>=85 and steering_angle<=95:
                Global.Direction == "F"
                ArduinoSerial.write(Global.Direction.encode())

            elif steering_angle>96:
                Global.Direction == "R"
                ArduinoSerial.write(Global.Direction.encode())
           
            elif steering_angle<84:
                Global.Direction == "L"
                ArduinoSerial.write(Global.Direction.encode())
            
            elif Global.Direction == "S":
                ArduinoSerial.write(Global.Direction.encode())
            
        cv2.waitKey(300)
    
        if cv2.waitKey(1) == ord( 'q' ):
            break

    cv2.destroyAllWindows()



if __name__ == '__main__':
    
    task1 = threading.Thread(target= Thread_Joystick)
    task2 = threading.Thread(target= Thread_CAM)

    task1.start()
    task2.start()
    


    
