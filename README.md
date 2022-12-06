# Final_project_autonomous_car

## 1. 프로젝트 개요

> 딥러닝 기반으로 움직이는 자율주행 RC카를 라즈베리파이와 아두이노를 연계하여 구현한다.

+ Bluetooth , Serial 통신을 이용하여 컨트롤러로 조종이 가능한 RC카 제작
+ tensorflow를 활용하여 CNN구조의 딥러닝 자율주행 RC카 구현 (tcp/ip 컴퓨터 통신~)
+ (추가) Can bus 통신으로 아두이노를 추가로 연결해 센서(초음파)를 이용한 데이터 수집 



## 2. 기술스택 과 구현환경

### <div align=center><h1>📚 STACKS</h1></div>
<div  align=center>
 <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
 <img src="https://img.shields.io/badge/arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white">
 <img src="https://img.shields.io/badge/raspberrypi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white">
 <img src="https://img.shields.io/badge/bluetooth-0082FC?style=for-the-badge&logo=bluetooth&logoColor=white">
 <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
 <br>
</div>

### <div align=center><h1>📚 IMPLEMENTATION ENVIRONMENT</h1></div>
<div  align=center>
 <img src="https://img.shields.io/badge/windows10-0078D6?style=for-the-badge&logo=windows10&logoColor=white">
 <img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
 <img src="https://img.shields.io/badge/arduino IDE-00979D?style=for-the-badge&logo=arduino IDE&logoColor=white">
 <img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visual studio code&logoColor=white">
 <br>
</div>

## 3. 시스템구조

![Temporary arrangement](https://user-images.githubusercontent.com/112140869/205536290-7488ffc0-9a94-419a-8fc0-16ecd72a8f46.png)

## 4. Project

+ Serial 통신을 활용한 제어 시스템칸 데이터 교환 & 제어 연계 시스템 구축
+ Tenserflow 와 OpenCV를 활용한 이미지 인식 딥러닝 구현
+ ps4 듀얼 쇼크와 bluetooth 통신하여 RC 카 제어

### 4.1 Serial 및 Bluetooth 통신
#### 4.1.1 RPI4 serial 및 bluetooth
 1. Threading, serial 라이브러리와 pyPS4Controller 라이브러리 사용
 2. 시리얼 포트 ttyACM0 포트로 아두이노 시리얼 통신
 3. ps4 듀얼 쇼크4 를 사용하기 위한 Class 생성 및 Class 상속 사용
 4. ps4 듀얼 쇼크4 포트 js0 포트로 Bluetooth 통신
---
헤더파일 및 전역변수
```python
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

strdata = "on_x_press"
IMGpath ="/home/pi/project/Finalproject/Track_Img/"

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
```
---
ps4 듀얼 쇼크4 사용을 위한 MyController 클래스 및 Global 클래스
```python
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
```
---
조이스틱 Thread
```python
def Thread_Joystick():

    controller.listen()

    while True:
                
        controller.on_up_arrow_press()

        controller.on_down_arrow_press()
                
        controller.on_left_arrow_press()

        controller.on_right_arrow_press()
```
---
opencv로 카메라 제어 Thread
```python
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
```
---
Thread 시작
```python
if __name__ == '__main__':
    
    task1 = threading.Thread(target= Thread_Joystick)
    task2 = threading.Thread(target= Thread_CAM)

    task1.start()
    task2.start()
```
---
#### 4.1.2 Arduino Mega Serial 통신
 1. ttyACM0 포트로 시리얼 통신
 2. serialEvent 함수 사용
---
시리얼 통신을 통해서 데이터가 입력될 때 자동으로 호출되는 함수인 serialEvent 함수
```c++
void serialEvent(){
    while (Serial.available())
    {
        char read_data  = Serial.read();

        switch(read_data){
            case 'F':
                _Forward();
                break;
            case 'B':
                _Back();
                break;
            case 'L':
                _Left();
                break;
            case 'R':
                _Right();
                break;
            case 'S':
                _Stop();
                break;

        }

    }
}
```
---
### 4.2 
 1.수집한 데이터로 모델을 딥러닝
 2.실시간 데이터를 모델에 적용하여 자율주행 구현

---
헤더파일 및 전역변수
 ```python
import os
import random
import fnmatch
import datetime
import pickle

#data processing
import numpy as np
np.set_printoptions(formatter={'float_kind : lambda x: "%.4f' })

import pandas as pd
pd.set_option('display.width',320)
pd.set_option('display.float_format','{:,.4f}'.format)
pd.set_option('display.max_colwidth',160)

#tensorflow
import tensorflow as tf
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,MaxPool2D,Dropout,Flatten,Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

print(f'tf.__version__: {tf.__version__}')
print(f'.keras.__version__: {tensorflow.keras.__version__}')

#sklearn
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

#imaging
import cv2
from imgaug import augmenters as img_aug
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#matplotlib inline
from PIL import Image
---
 모델 
 ```python
def my_imread(image_path):
    image = cv2.imread(image_path)
    return image

def img_preprocess(image):
    image = image/255
    return image

def nvidia_model():
    model = Sequential(name ='Nvidia_Model')

    model.add(Conv2D(24,(5,5),strides=(2,2), input_shape=(80, 320, 3), activation ='elu'))
    model.add(Conv2D(36,(5,5),strides=(2,2), activation ='elu'))
    model.add(Conv2D(48,(5,5),strides=(2,2), activation ='elu'))
    model.add(Conv2D(64,(5,5), activation ='elu'))
    model.add(Dropout(0.2))
    model.add(Conv2D(64, (3,3), activation ='elu'))

    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))

    model.add(Dense(1))

    # Cus_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss='mse', optimizer='adam')

    return model

def image_data_generator(image_paths, steering_angles, batch_size):
    while True:
        batch_images =[]
        batch_steering_angles = []

        for i in range(batch_size):
            random_index = random.randint(0,len(image_paths)-1)
            image_path = image_paths[random_index]
            image = my_imread(image_paths[random_index])
            steering_angle = steering_angles[random_index]

            image = img_preprocess(image)
            batch_images.append(image)
            batch_steering_angles.append(steering_angle)

        yield(np.asarray(batch_images),np.asarray(batch_steering_angles))


---
수집한 데이터 전처리 및 모델 

 ```python
data_dir = "C:\\Users\\KOSTA\\tensorflow\\video"
file_list = os.listdir(data_dir)
image_paths=[]
steering_angle =[]
pattern = "*png"
for filename in file_list:
    if fnmatch.fnmatch(filename,pattern):
        image_paths.append(os.path.join(data_dir,filename))
        angle = int(filename[-7:-4])
        steering_angle.append(angle)

image_index =10
plt.imshow(Image.open(image_paths[image_index]))
print("image_path: %s" %image_paths[image_index])
print("steering_Angle: %d" %steering_angle[image_index])
Image_change_Angle = pd.DataFrame()
Image_change_Angle['ImagePath'] = image_paths
Image_change_Angle['Angle'] = steering_angle

num_of_bins = 25
hist, bins = np.histogram(Image_change_Angle['Angle'],num_of_bins)

# fig, axes = plt.subplots(1,1,figsize=(12,4))
# axes.hist(Image_change_Angle['Angle'],bins=num_of_bins,width=1,color='blue')

##plt.show()

X_train, X_valid, y_train, y_valid = train_test_split( image_paths, steering_angle, test_size=0.2)
print("Trainin data: %d\n Validation data: %d" %(len(X_train), len(X_valid)))

# fig, axes = plt.subplots(1,2,figsize =(12,4))
# axes[0].hist(y_train,bins = num_of_bins, width=1,color ='blue')
# axes[0].set_title('Training Data')
# axes[1].hist(y_valid, bins = num_of_bins, width =1, color = 'red')
# axes[1].set_title('Validation Data')


# fig, axes = plt.subplots(1, 2,figsize=(15,10))
# image_orig = my_imread(image_paths[image_index])
# image_processed = img_preprocess(image_orig)

# axes[0].imshow(image_orig)
# axes[0].set_title("orig")
# axes[1].imshow(image_processed)
# axes[1].set_title("processed")

model =nvidia_model()
print(model.summary())
#plt.show()

ncol =2
nrow =2

X_train_batch,y_train_batch =next(image_data_generator(X_train,y_train,nrow))
X_valid_batch,y_valid_batch =next(image_data_generator(X_valid,y_valid,nrow))

fig, axes =plt.subplots(nrow,ncol,figsize=(15,6))
fig.tight_layout()

for i in range(nrow):
    axes[i][0].imshow(X_train_batch[i])
    axes[i][0].set_title("traing, angle=%s" % y_train_batch[i])
    axes[i][1].imshow(X_valid_batch[i])
    axes[i][1].set_title("validation, angle=%s" % y_valid_batch[i])

model_output_dir = 'C:\\Users\\KOSTA\\tensorflow\\AI_data'

checkpoint_callback = tensorflow.keras.callbacks.ModelCheckpoint(filepath=os.path.join(model_output_dir,'lane_navigation_check.h5'),verbose=1,save_best_only=True)

history = model.fit_generator(image_data_generator(X_train,y_train, batch_size =100),steps_per_epoch=300,epochs=10,validation_data=image_data_generator(X_valid,y_valid,batch_size=100),validation_steps=200,verbose=1,shuffle=1,callbacks=[checkpoint_callback])

model.save(os.path.join(model_output_dir,'lane_navigation_final.h5'))

history_path = os.path.join(model_output_dir,'history.pickle')
with open(history_path,"wb") as f:
    pickle.dump(history.history,f,pickle.HIGHEST_PROTOCOL)


from sklearn.metrics import mean_squared_error, r2_score
---
결과 확인하기
 ```python
 
history.history

history_path = os.path.join(model_output_dir,'history.pickle')
with open(history_path,'rb') as f:
    history = pickle.load(f)

history
plt.plot(history['loss'],color='blue')
plt.plot(history['val_loss'],color = 'red')
plt.legend(['training loss', 'validation loss'])

def summarize_prediction(Y_true,Y_pred):

    mse = mean_squared_error(Y_true,Y_pred)
    r_squared = r2_score(Y_true,Y_pred)

    print(f' mse = {mse:.2}')
    print(f' r_squared = {r_squared:.2%}')
    print()

def predict_and_summarize(X,Y):
    model = load_model(f' {model_output_dir}/lane_navigation_check.h5')
    Y_pred = model.predict(X)
    summarize_prediction(Y,Y_pred)
    return Y_pred

n_tests =100
X_test,y_test = next(image_data_generator(X_valid,y_valid, 100))

y_pred = predict_and_summarize(X_test,y_test)

n_tests_show =2
fig, axes = plt.subpplots(n_tests_show,1,figsize(10,4*n_tests_show))

for i in range(n_tests_show):
    axes[i].imshow(X_test[i])
    axes[i].set_title(f' actual angle={y_test[i]}, predicted angle ={int(y_pred[i])}, diff ={int(y_pred[i])-y_test[i]}')

plt.show()
```
---
 실시간 자율주행 (구현 실패)

 
---
### 4.3 Arduino 초음파 CAN 통신
 1. Interrupt를 사용한 데이터 수신
 2. MCP2515-lib-master 라이브러리 및 SPI 라이브러리 사용
#### 4.3.1 Arduino Uno CAN 및 초음파
---
헤더파일 및 전역변수
```c++
#include <SPI.h>
#include <mcp_can.h>

#define spiCSPin 10

#define TRIGPin 9
#define ECHOPin 8

MCP_CAN CAN(spiCSPin);
```
---
Interrupt 발생 시 동작하는 함수
```c++
void CAN_INT(){
    unsigned char len = 0;
    unsigned char buf[8];
    

    CAN.readMsgBuf(&len,buf); // CAN 데이터 가져오기
    unsigned long canId = CAN.getCanId(); // CAN ID 얻기
    switch (canId)
    {
    case 0x80:
        Serial.print("\nData from ID : 0x");
        Serial.println(canId,HEX); // 16진수로 ID 출력
        for(int i=0;i<len;i++){
            Serial.print(buf[i]);
            Serial.print("\t");
        }
        Serial.print("\n");
        
        break;
    
    default:
        break;
    }
    
}
```
---
초음파 데이터
```c++
float read_Ultrasonic() {
    float return_time;
    float time_took;
    
    digitalWrite(TRIGPin, HIGH);
    
    delay(5);
    
    digitalWrite(TRIGPin, LOW);
    
    return_time = pulseIn(ECHOPin, HIGH);
    time_took = 340.0f * return_time / 10000.0f / 2.0f;
    
    return time_took;
}
```
---
초음파 데이터 전송
```c++
void Send_Ultrasonic_data(){
    distance_union du;
    unsigned char data[8];

    du.first = read_Ultrasonic();
    for(int i=0; i<8; i++){
        data[i] = du.second[i];
    }

    CAN.sendMsgBuf(0x90,0,8,data);
    delay(250);
}
```
---
setup 설정 및 Interrupt 설정
```c++
void setup(){
    Serial.begin(115200);
    init_Ultrasonic();
    
    while ( CAN_OK != CAN.begin(CAN_500KBPS))
    {
        Serial.println("CAN BUS init Failed");
        delay(100);
    }
    Serial.println("CAN BUS Shield Init OK!");

    attachInterrupt(digitalPinToInterrupt(2),CAN_INT,FALLING);
    
}
```
---
loop 설정
```c++
void loop(){
    Send_Ultrasonic_data();
}
```
---
#### 4.3.2 Arduino Mega CAN 통신
---
헤더파일 및 전역변수
```c++
#include <SPI.h>
#include <mcp_can.h>

#define spiCSPin_mega 53

MCP_CAN CAN(spiCSPin_mega);
```
---
Interrupt 발생 시 동작하는 함수
```c++
void CAN_INT(){
    unsigned char len = 0;
    unsigned char buf[8];
    

    CAN.readMsgBuf(&len,buf); // CAN 데이터 가져오기
    unsigned long canId = CAN.getCanId(); // CAN ID 얻기
    switch (canId)
    {
    case 0x90:
        Serial.print("\nData from ID : 0x");
        Serial.println(canId,HEX); // 16진수로 ID 출력
        for(int i=0;i<len;i++){
            Serial.print(buf[i]);
            Serial.print("\t");
        }
        Serial.print("\n");
        
        break;
    
    default:
        break;
    }
    
}
```
---
setup 설정 및 Interrupt 설정
```c++
void setup() {

    Serial.begin(115200);
    init_Motor();

    while ( CAN_OK != CAN.begin(CAN_500KBPS))
    {
        Serial.println("CAN BUS init Failed");
        delay(100);
    }
    Serial.println("CAN BUS Shield Init OK!");

    attachInterrupt(digitalPinToInterrupt(2),CAN_INT,FALLING);

}
```
---
loop 설정
초음파로 측정한 거리값 20 이하일 시 모터 정지
```c++
void loop() {
    if(ultra_distance <= 20.00){
        _Stop();
    }
    
}
```
---


## 5. 구현 결과 & 결론

## 참고 자료

+ 라즈베리파이 아두이노 시리얼 통신

  + https://jcdgods.tistory.com/525

  + https://throwexception.tistory.com/920

  + http://www.3demp.com/community/boardDetails.php?cbID=232

  + https://jung-max.github.io/2020/06/15/Python-serial/
  
+ 라즈베리파이 아두이노 블루투스 연결

  + https://monotics.tistory.com/28
  
  + https://raspberrypi.stackexchange.com/questions/121216/how-to-best-handle-raspberry-pi-4-and-smartphone-connection-over-bluetooth-and-p
  
  + https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=beaqon&logNo=221411638205
  
  + https://stackoverflow.com/questions/36099960/how-to-connect-to-raspberry-pi-with-an-android-app-over-bluetooth
  
  + https://koboogy.tistory.com/8
  
+ 라즈베리파이 Opencv 카메라 이미지 처리

  + https://diyver.tistory.com/61
  
  + https://opencv-python.readthedocs.io/en/latest/doc/09.imageThresholding/imageThresholding.html
  
  + https://scribblinganything.tistory.com/473
  
  + https://webnautes.tistory.com/1270
  
  + https://m.blog.naver.com/samsjang/220516822775

  + https://diy-project.tistory.com/115

  + https://codezaram.tistory.com/44?category=1281352

  + https://github.com/lky9620/Ta-Yo/blob/main/Raspberry-Pi/line_detect.py
  
+ 기술 스택
  + https://cocoon1787.tistory.com/689

+ L293D Shield 모터 제어
  + https://eleit.tistory.com/entry/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%EB%AA%A8%ED%84%B0%EC%89%B4%EB%93%9C-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-DC%EB%AA%A8%ED%84%B0-%EA%B5%AC%EB%8F%99%ED%95%98%EA%B8%B0
  + https://m.blog.naver.com/eduino/220884056251

+ String int 변환
  + https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=kim-nan-hee&logNo=221954492559

+ arduno String 문자열 분열
  + https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=okarduino&logNo=220762181563
  
+ while문 참고
  + https://sagittariusof85s.tistory.com/143

+ 라즈베리파이 부팅시 프로그램 자동 실행
  + https://m.blog.naver.com/emperonics/221770579539

+ 텐서플로우 

  + https://blog.naver.com/PostView.naver?blogId=beodeulpiri&logNo=222846798881&parentCategoryNo=&categoryNo=37&viewDate=&isShowPopularPosts=true&from=search
  
  + https://dyddl1993.tistory.com/34
  
  + https://velog.io/@mythos/Raspberry-Pi-4-Python-%EB%B2%84%EC%A0%84-%EA%B4%80%EB%A6%AC
  
  + https://dreamtip.tistory.com/18
  
  + https://lindevs.com/install-precompiled-tensorflow-lite-on-raspberry-pi (tensorflow lite)
  
  + https://qengineering.eu/install-tensorflow-2.4.0-on-raspberry-64-os.html

+ Opencv 버전 변경
  + https://nuggy875.tistory.com/86
  
+ can 통신

  + https://memories.tistory.com/129
  
  + https://makeutil.tistory.com/95
  
  + https://blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=mts90&logNo=221542266246&parentCategoryNo=&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView

  + https://forum.arduino.cc/t/canbus-shield-can-init-failing/867955
  
+ Rx Tx serial 통신
  
  + https://oscarliang.com/raspberry-pi-and-arduino-connected-serial-gpio/

+ pyPS4Controller

  + https://github.com/ArturSpirin/pyPS4Controller

+ 모바일 VNC Viewer

  + https://digital-play.tistory.com/30

+ python class 정적변수
  
  + https://zetawiki.com/wiki/%ED%8C%8C%EC%9D%B4%EC%8D%AC_%EC%A0%84%EC%97%AD%EB%B3%80%EC%88%98%EB%A5%BC_%ED%81%B4%EB%9E%98%EC%8A%A4_%EC%A0%95%EC%A0%81%EB%B3%80%EC%88%98%EB%A1%9C_%EA%B5%AC%ED%98%84

+ VScode 가상환경 설정

  + https://useful-jang.tistory.com/74

+ 초음파 거리계산

  + https://blog.naver.com/PostView.naver?blogId=lline_edu&logNo=222219099428
