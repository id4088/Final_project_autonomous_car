# Final_project_autonomous_car

## 1. 프로젝트 개요

> 딥러닝 기반으로 움직이는 자율주행 RC카를 라즈베리파이와 아두이노를 연계하여 구현한다.

+ Bluetooth , Serial 통신을 이용하여 컨트롤러로 조종이 가능한 RC카 제작
+ tensorflow를 활용하여 CNN구조의 딥러닝 자율주행 RC카 구현 (tcp/ip 컴퓨터 통신~)
+ (추가) Can bus 통신으로 아두이노를 추가로 연결해 센서(초음파)를 이용한 데이터 수집 



## 2. 기술스택 과 구현환경

### 📚 STACKS

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white">
<img src="https://img.shields.io/badge/raspberrypi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white">
<img src="https://img.shields.io/badge/bluetooth-0082FC?style=for-the-badge&logo=bluetooth&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">

### 📚 IMPLEMENTATION ENVIRONMENT

<img src="https://img.shields.io/badge/windows10-0078D6?style=for-the-badge&logo=windows10&logoColor=white">
<img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
<img src="https://img.shields.io/badge/arduino IDE-00979D?style=for-the-badge&logo=arduino IDE&logoColor=white">
<img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visual studio code&logoColor=white">

## 3. 시스템구조

![Temporary arrangement](https://user-images.githubusercontent.com/112140869/205536290-7488ffc0-9a94-419a-8fc0-16ecd72a8f46.png)

## 4. Project

+ Serial 통신을 활용한 제어 시스템칸 데이터 교환 & 제어 연계 시스템 구축
+ Tenserflow 와 OpenCV를 활용한 이미지 인식 딥러닝 구현
+ Bluetooth 통신 기반 원격 제어 (?)

### 4.1 Serial 및 Bluetooth 통신
#### 4.1.1 RPI4 serial 및 bluetooth
 1. Threading, serial 라이브러리와 pyPS4Controller 라이브러리 사용
 2. 시리얼 포트 ttyACM0 포트로 아두이노 시리얼 통신
 3. ps4 듀얼 쇼크4 를 사용하기 위한 Class 생성 및 Class 상속 사용
 4. ps4 듀얼 쇼크4 포트 js0 포트로 Bluetooth 통신
---
헤더파일 및 전역변수
```python
import threading
import serial , time
from pyPS4Controller.controller import Controller

ArduinoSerial = serial.Serial(port = "/dev/ttyACM0", 
	baudrate= 115200,
	timeout= 1)

strdata = "on_x_press"

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
### 4.2 

### 4.3 


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
