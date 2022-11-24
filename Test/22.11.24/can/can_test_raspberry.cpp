#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <fcntl.h> // 파일 처리를 위한 헤더파일
#include <unistd.h> // POSIX 운영체제 API 엑세스 제공 헤더파일

#include <pthread.h> // 쓰레드 헤더파일
#include <arpa/inet.h> // hton, ntoh , htons, ... etc

#include <sys/socket.h> // socket, bind, listen, ...
#include <sys/types.h>
#include <sys/ioctl.h>
#include <netinet/in.h> // sockaddr_in 
#include <net/if.h>

#include <stdint.h>

#include <linux/can.h>
#include <linux/can/raw.h>



int led_green = 23;
int led_blue = 24;

int btn_green = 20;
int btn_blue = 21;

/* ============== GLOBAL variables ============== */
static int can_socket; // CAN socket
static struct sockaddr_can addr;
static struct ifreq ifr; // ifreq structure contaning the interface name
/* ============================================== */


void init_bind_socket_can(){

	/* ======================  Create Socket using 3 parameters ======================
	domain/protocol family(PF_CAN), type of socket(raw or datagram),socket protocol */
	if((can_socket=socket(PF_CAN,SOCK_RAW,CAN_RAW)) < 0){
		perror("Socket");
		return;
	}

	/* Retrieve the interface index for the interface name(can0, can1, vcan0, etc ... ) */
	strcpy(ifr.ifr_name,"can0");

	/* 네트워크 관리 스택 접근을 위한 I/O controll, 사용자 영역에서 커널 영역의 데이터 접근(system call) using 3 parameters
	an open file descriptor(s), request code number(SIOCGIFINDEX), value */
	ioctl(can_socket,SIOCGIFINDEX,&ifr);

	// Bind Socket to the CAN interface
	memset(&addr,0,sizeof(addr));
	addr.can_family = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	if (bind(can_socket,(struct sockaddr *)&addr, sizeof(addr)) < 0){
		perror("Bind");
		return;
	}

	printf("CAN Socket creation & bind success!\n");
}


void* thread_func(void* arg){
    int nBytes;
    int csock = *((int*)arg);
    struct can_frame recieve_frame;

    nBytes = read(csock,&recieve_frame,sizeof(struct can_frame));
    printf("%d", nBytes);
    if(nBytes < 0){
        perror("Read");
        return NULL;
    }

    switch(recieve_frame.can_id){
        case 0x90:
            printf("Distance COM9\n");
            printf("0x%2X {%d} ",recieve_frame.can_id,recieve_frame.can_dlc);
            for(int i=0;i<recieve_frame.can_dlc;i++){
                printf("%X Cm",recieve_frame.data[i]);
            }
            printf("\r\n");

            break;

        case 0x91:
            printf("Distance COM3\n");
            printf("0x%2X {%d} ",recieve_frame.can_id,recieve_frame.can_dlc);
            for(int i=0;i<recieve_frame.can_dlc;i++){
                printf("%X Cm",recieve_frame.data[i]);
            }
            printf("\r\n");

            break;
        default:
            break;
    }
    
}


// void* thread_send_func(void* arg){
//     int csock = *((int*)arg);
//     struct can_frame send_frame;

//     while(1){
//         // code 작성하기
        
//         send_frame.can_id = 0x92;
//         send_frame.can_dlc = 8;
          
//         if(write(csock, &send_frame, sizeof(struct can_frame)) != sizeof(struct can_frame)){
//             perror("Write");
//             return NULL;           
//         }
//         sleep(0.5);
//         continue;
//     }
// }




int main(){
    
    pthread_t thread;
    pthread_t send_thread;

    struct can_frame recieve_frame;
    struct can_frame send_frame;

    init_bind_socket_can(); // 소켓 초기화

    // 송신 전용 쓰레드 생성
    // pthread_create(&send_thread,NULL,thread_send_func,&can_socket);

    // 무한 루프를 돌며 쓰레드를 사용해 데이터 수신
    while(1){
        pthread_create(&thread,NULL,thread_func,&can_socket);
        printf("thread_id : %lx\n",thread);
        sleep(1);
        // pthread_join(thread,NULL);
    }


    if (close(can_socket) < 0) {
		perror("Close");
		return 1;
	}

}
