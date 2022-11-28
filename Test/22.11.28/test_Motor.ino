#include <AFMotor.h>

AF_DCMotor FRmotor(2);
AF_DCMotor FLmotor(1);
AF_DCMotor BLmotor(4);
AF_DCMotor BRmotor(3);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  Serial.println("Motor Test");



  FRmotor.setSpeed(110);
  FLmotor.setSpeed(110);
  BRmotor.setSpeed(110);
  BLmotor.setSpeed(110);

  FRmotor.run(RELEASE);
  FLmotor.run(RELEASE);
  BLmotor.run(RELEASE);
  BRmotor.run(RELEASE);

}

void loop() {
  // put your main code here, to run repeatedly:
  
}

void serialEvent(){
  while (Serial.available())
  {
    char a  = Serial.read();

//    int first = a.indexOf("_");
//    int second = a.indexOf("_",first + 1);
//    int length = a.length();
//
//    String b = a.substring(0, first);
//    String c = a.substring(first + 1, second);
//    
//    char e = b.charAt(0);
//    int d = c.toInt();

    // if(b == "Forward"){ _Forward(d); }
    // if(b == "Back"){ _Back(d); }
    // if(b == "Left"){ _Left(d); }
    // if(b == "Right"){ _Right(d); }
    // if(b == "Stop"){ _Stop(); }

    switch(a){
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

void _Forward(){

    FRmotor.run(BACKWARD);
    FLmotor.run(BACKWARD);
    BRmotor.run(BACKWARD);
    BLmotor.run(BACKWARD);
    FRmotor.setSpeed(45);
    FLmotor.setSpeed(45);
    BRmotor.setSpeed(45);
    BLmotor.setSpeed(45);
}

void _Back(){
    FRmotor.run(FORWARD);
    FLmotor.run(FORWARD);
    BRmotor.run(FORWARD);
    BLmotor.run(FORWARD);
    
    FRmotor.setSpeed(50);
    FLmotor.setSpeed(50);
    BRmotor.setSpeed(50);
    BLmotor.setSpeed(50);
}

void _Left(){
    FRmotor.run(BACKWARD);
    FLmotor.run(FORWARD);
    BRmotor.run(BACKWARD);
    BLmotor.run(FORWARD);
    
    FRmotor.setSpeed(150);
    FLmotor.setSpeed(60);
    BRmotor.setSpeed(165);
    BLmotor.setSpeed(70);
}

void _Right(){
    FRmotor.run(FORWARD);
    FLmotor.run(BACKWARD);
    BRmotor.run(FORWARD);
    BLmotor.run(BACKWARD);
    
    FRmotor.setSpeed(50);
    FLmotor.setSpeed(160);
    BRmotor.setSpeed(70);
    BLmotor.setSpeed(130);
}

void _Stop(){
    FRmotor.run(RELEASE);
    FLmotor.run(RELEASE);
    BLmotor.run(RELEASE);
    BRmotor.run(RELEASE);
}
