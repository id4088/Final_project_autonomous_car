#include <SPI.h>
#include <mcp_can.h>

#define spiCSPin 10

#define TRIGPin 9
#define ECHOPin 8

MCP_CAN CAN(spiCSPin);

union distance_union{
    float first;
    unsigned char second[8];
};

void init_Ultrasonic(){
    pinMode(TRIGPin, OUTPUT);
    pinMode(ECHOPin, INPUT);
}

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

void setup(){
    Serial.begin(115200);
    init_Ultrasonic();
    
    while ( CAN_OK != CAN.begin(CAN_500KBPS))
    {
        Serial.println("CAN BUS init Failed");
        delay(100);
    }
    Serial.println("CAN BUS Shield Init OK!");
    
}


void loop(){
    Send_Ultrasonic_data();
}
