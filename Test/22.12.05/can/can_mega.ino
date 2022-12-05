
#include <AFMotor.h>
#include <SPI.h>
#include <mcp_can.h>

#define spiCSPin 10
#define spiCSPin_mega 53

MCP_CAN CAN(spiCSPin_mega);

AF_DCMotor FRmotor(2);
AF_DCMotor FLmotor(1);
AF_DCMotor BLmotor(4);
AF_DCMotor BRmotor(3);

union distance_union{
    float first;
    unsigned char second[8];
};

static float ultra_distance;

void init_Motor(){
    FRmotor.run(RELEASE);
    FLmotor.run(RELEASE);
    BLmotor.run(RELEASE);
    BRmotor.run(RELEASE);

    FRmotor.setSpeed(110);
    FLmotor.setSpeed(110);
    BRmotor.setSpeed(110);
    BLmotor.setSpeed(110);

    Serial.println("Motor init Success!");
}

void _Forward(){
    if(ultra_distance > 20.00){
        FRmotor.run(BACKWARD);
        FLmotor.run(BACKWARD);
        BRmotor.run(BACKWARD);
        BLmotor.run(BACKWARD);
        FRmotor.setSpeed(45);
        FLmotor.setSpeed(45);
        BRmotor.setSpeed(45);
        BLmotor.setSpeed(45);
    }
    
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
    if(ultra_distance > 20.00){
        FRmotor.run(BACKWARD);
        FLmotor.run(FORWARD);
        BRmotor.run(BACKWARD);
        BLmotor.run(FORWARD);
        
        FRmotor.setSpeed(150);
        FLmotor.setSpeed(60);
        BRmotor.setSpeed(165);
        BLmotor.setSpeed(70);
    }
    
}

void _Right(){
    if(ultra_distance > 20.00){
        FRmotor.run(FORWARD);
        FLmotor.run(BACKWARD);
        BRmotor.run(FORWARD);
        BLmotor.run(BACKWARD);
        
        FRmotor.setSpeed(50);
        FLmotor.setSpeed(160);
        BRmotor.setSpeed(70);
        BLmotor.setSpeed(130);
    }
    
}

void _Stop(){
    FRmotor.run(RELEASE);
    FLmotor.run(RELEASE);
    BLmotor.run(RELEASE);
    BRmotor.run(RELEASE);
}

void CAN_INT(){
    unsigned char len = 0;
    unsigned char buf[8];
    

    CAN.readMsgBuf(&len,buf); // CAN 데이터 가져오기
    unsigned long canId = CAN.getCanId(); // CAN ID 얻기
    switch (canId)
    {
    case 0x90:
        distance_union d;
        

        Serial.print("\nData from ID : 0x");
        Serial.println(canId,HEX); // 16진수로 ID 출력
        for(int i=0;i<len;i++){
            d.second[i] = buf[i];
        }
        ultra_distance = d.first;
        Serial.print(ultra_distance);
        Serial.print(" CM\n");
        break;
    
    default:
        break;
    }
    
}

void setup() {
    // put your setup code here, to run once:
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

void loop() {
    // put your main code here, to run repeatedly:
    if(ultra_distance <= 20.00){
        _Stop();
    }
    
}

void serialEvent(){
    while (Serial.available())
    {
        char a  = Serial.read();

        // int first = a.indexOf("_");
        // int second = a.indexOf("_",first + 1);
        // int length = a.length();

        // String b = a.substring(0, first);
        // String c = a.substring(first + 1, second);
        
        // char e = b.charAt(0);
        // int d = c.toInt();

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
