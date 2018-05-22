#include <stdio.h>
#include <stdlib.h>		
#include <string.h>		//包含bzero等函数
#include <unistd.h>

#include <sys/types.h>
#include <sys/socket.h> //包含协议族的宏定义
#include <arpa/inet.h>
#include <net/ethernet.h>
#include <netinet/if_ether.h>
#include <netpacket/packet.h>
#include <net/if.h>

#include <sys/ioctl.h>
#define DEBUG

const char* NIC1 = "wlp2s0";
const char* NIC2 = "enp3s0";
const char* NIC3 = "lo";

void print_byte(unsigned char* buff,int len,char* notice)
{/*以16进制的形式打印从buff开始的len字节内存，notice会作为提示显示在数据前面*/
    int i;
    printf("%s(0x):",notice);
    for(i=0;i<len;i++){
		printf("%02x-",buff[i]);
		if((i+1) % 16 == 0){
			printf("\b \n");
        }
	}
    if(i%16 != 0){
        printf("\b \n");
    }
}

int getNICIndex(const char* NIC_name, struct ifreq* ifr, int sockfd){
    size_t if_name_len = strlen(NIC_name);
    if(if_name_len < sizeof(ifr->ifr_name)){
        memcpy(ifr->ifr_name, NIC_name, if_name_len);
        ifr->ifr_name[if_name_len] = '\0';
    }
    if(ioctl(sockfd, SIOCGIFINDEX, ifr) == -1){
        perror("Error when finding device");
        return -1;
    }
    return ifr->ifr_ifindex;
}

int getHWAddr(struct ifreq* ifr, int sockfd){
    if(ioctl(sockfd, SIOCGIFHWADDR, ifr) == -1){
        perror("Error when finding device");
        return -1;
    }
    return 0;
}

void packAddr(struct sockaddr_ll* addr, int ifindex){
    addr->sll_family = AF_PACKET;
    addr->sll_ifindex = ifindex;
    addr->sll_halen = ETHER_ADDR_LEN;
    addr->sll_protocol = htons(ETH_P_ALL);
    //memcpy(addr.sll_addr, dest, ETH_ALEN); //好像不需要这个
}

int cmpAddr(unsigned char* addr1, unsigned char* addr2){
    int i;
    for(i=0; i<6; i++){
        if(addr1[i] != addr2[i])
            return 0;
    }
    return 1;
}

int main(){
    int i;
    int send_sockfd, recv_sockfd;
    socklen_t sockaddr_ll_len = sizeof(struct sockaddr_ll);
    int recv_f_len, send_f_len;
    int send_ifindex, recv_ifindex;
    unsigned char ef[ETH_FRAME_LEN];
    struct ethhdr* p_ethhdr;
    unsigned char source[ETH_ALEN];
    unsigned char dest[3][ETH_ALEN] = 
    {
        {0x58, 0x69, 0x6c, 0x91, 0x09, 0x1a},
        {0x44, 0x44, 0x44, 0x44, 0x44, 0x44},
        {0x77, 0x77, 0x77, 0x77, 0x77, 0x77}
    };
    
    

    send_sockfd = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if(send_sockfd == -1){
        perror("socket created failed");
        exit(EXIT_FAILURE);
    }
    recv_sockfd = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if(recv_sockfd == -1){
        perror("socket created failed");
        exit(EXIT_FAILURE);
    }


    //获取网卡索引号
    struct ifreq ifr;

    recv_ifindex = getNICIndex(NIC1, &ifr, recv_sockfd);
    send_ifindex = getNICIndex(NIC1, &ifr, send_sockfd);
    getHWAddr(&ifr, send_ifindex);
    print_byte(ifr.ifr_hwaddr.sa_data, 6 ,"addr");
    memcpy(source, ifr.ifr_hwaddr.sa_data, 6);

    //填充sockaddr_ll型地址
    struct sockaddr_ll send_addr = {0};
    packAddr(&send_addr, send_ifindex);

    struct sockaddr_ll recv_addr = {0};
    packAddr(&recv_addr, recv_ifindex);

    if(bind(send_sockfd, (struct sockaddr*)&send_addr, sizeof(send_addr)) == -1){
        perror("bind error");
    }
    if(bind(recv_sockfd, (struct sockaddr*)&recv_addr, sizeof(recv_addr)) == -1){
        perror("bind error");
    }


    
    while(1){
        //接收数据包
        recv_f_len = recv(recv_sockfd, ef,ETH_FRAME_LEN, 0);

        //读取包信息
        p_ethhdr = (struct ethhdr*)ef;
        if(cmpAddr(p_ethhdr->h_source, source)){
            continue;
        }
        #ifdef DEBUG
        printf("%d bytes received\n", recv_f_len);
        print_byte(p_ethhdr->h_dest, 6, "destination");
        print_byte(p_ethhdr->h_source, 6, "source");
        #endif

        //修改以太网帧
        memcpy(p_ethhdr->h_source, source, ETH_ALEN);
        //选择目标click
        int des_click_sn = (rand() * 10) % 3;
        memcpy(p_ethhdr->h_dest, dest[des_click_sn], ETH_ALEN);

        
        //发送数据包
        send_f_len = send(send_sockfd, ef, recv_f_len, 0);
        if(send_f_len == -1){
            perror("send failed");
        }else{
            #ifdef DEBUG
            printf("%d bytes sent\n", send_f_len);
            #endif
        }
        
    }
    

    
    
    return 0;
}