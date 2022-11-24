#include <SPI.h>
#include <mcp_can.h>

#define spiCSPin 10

#define TRIGPin 9
#define ECHOPin 8

MCP_CAN CAN(spiCSPin);

void CAN_INT(){
    unsigned char len = 0;
    unsigned char buf[8];
    

    CAN.readMsgBuf(&len,buf); // CAN 데이터 가져오기
    unsigned long canId = CAN.getCanId(); // CAN ID 얻기
    switch (canId)
    {
    case 0x91:
        Serial.print("\nData from ID : 0x");
        Serial.println(canId,HEX); // 16진수로 ID 출력
        for(int i=0;i<len;i++){
            Serial.print(buf[i]);
            Serial.print("\t");
        }
        Serial.print("\n");
        
        break;
    
    case 0x92:
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

void setup(){
    Serial.begin(115200);
    pinMode(TRIGPin, OUTPUT);
    pinMode(ECHOPin, INPUT);
    
    while ( CAN_OK != CAN.begin(CAN_500KBPS,MCP_8MHz))
    {
        Serial.println("CAN BUS init Failed");
        delay(100);
    }
    Serial.println("CAN BUS Shield Init OK!");

    attachInterrupt(digitalPinToInterrupt(2),CAN_INT,FALLING);
    
}


void loop(){
    long duration;
    int distance;
    
    digitalWrite(TRIGPin, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGPin, LOW);

    duration = pulseIn(ECHOPin, HIGH);

    distance = duration * 17 / 1000;
        
    // Serial.print(distance);
    // Serial.println(" cm");

    unsigned char USdistancd = distance;

    unsigned char data[8] = {USdistancd};
    CAN.sendMsgBuf(0x90, 0, 8, data);
    delay(1000);
}
