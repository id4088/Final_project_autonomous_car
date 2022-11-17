#include <AFMotor.h>

AF_DCMotor FRmotor(1);
AF_DCMotor FLmotor(2);
AF_DCMotor BLmotor(3);
AF_DCMotor BRmotor(4);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Motor Test");

  FRmotor.setSpeed(100);
  FLmotor.setSpeed(100);
  BRmotor.setSpeed(100);
  BLmotor.setSpeed(100);

  FRmotor.run(RELEASE);
  FLmotor.run(RELEASE);
  BLmotor.run(RELEASE);
  BRmotor.run(RELEASE);
}

void loop() {
  // put your main code here, to run repeatedly:
  String a  = Serial.readString();

  int first = a.indexOf("_");
  int second = a.indexOf("_",first + 1);
  int length = a.length();

  String b = a.substring(0, first);
  String c = a.substring(first + 1, second);
    
  int d = b.toInt();
  
  if(c == "forward"){
    FRmotor.run(FORWARD);
    FLmotor.run(FORWARD);
    BRmotor.run(FORWARD);
    BLmotor.run(FORWARD);
    FRmotor.setSpeed(d);
    FLmotor.setSpeed(d);
    BRmotor.setSpeed(d);
    BLmotor.setSpeed(d);
  }
  else if( c == "stop"){
    FRmotor.run(RELEASE);
    FLmotor.run(RELEASE);
    BLmotor.run(RELEASE);
    BRmotor.run(RELEASE);
  }
  else if( c == "back" ){
    FRmotor.run(BACKWARD);
    FLmotor.run(BACKWARD);
    BRmotor.run(BACKWARD);
    BLmotor.run(BACKWARD);

    FRmotor.setSpeed(d);
    FLmotor.setSpeed(d);
    BRmotor.setSpeed(d);
    BLmotor.setSpeed(d);
  }
  else if( c == "right" ){
    FRmotor.run(BACKWARD);
    FLmotor.run(FORWARD);
    BRmotor.run(BACKWARD);
    BLmotor.run(FORWARD);
    
    FRmotor.setSpeed(d);
    FLmotor.setSpeed(d);
    BRmotor.setSpeed(d);
    BLmotor.setSpeed(d);
  }
  else if( c == "left" ){
    FRmotor.run(FORWARD);
    FLmotor.run(BACKWARD);
    BRmotor.run(FORWARD);
    BLmotor.run(BACKWARD);
    
    FRmotor.setSpeed(d);
    FLmotor.setSpeed(d);
    BRmotor.setSpeed(d);
    BLmotor.setSpeed(d);
  }
  

}
