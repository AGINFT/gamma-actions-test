# 🜚 MISSION BRAIN V22 🜚
import os, subprocess, time, requests, socket

def execute_mission(ui, ID):
    ui.log('Cargando Motor Real Strike V22...')
    c_src = """#include <stdio.h>
#include <openssl/sha.h>
#include <openssl/ripemd.h>
#include <openssl/ec.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
unsigned char t[20]={0x2b,0x6f,0x17,0xe0,0x89,0x29,0xe7,0x93,0xef,0x1c,0x09,0x93,0x0e,0x13,0x71,0xba,0x76,0x35,0xc6,0x0c};
void* c(void* a){
    EC_GROUP* g=EC_GROUP_new_by_curve_name(714);
    EC_POINT* p=EC_POINT_new(g);
    BIGNUM* k=BN_new();
    unsigned char b[65],s[32],r[20];
    BN_hex2bn(&k,"0618E107618E107618E107618E107618E107618E107618E107618E107");
    while(1){
        EC_POINT_mul(g,p,k,NULL,NULL,NULL);
        EC_POINT_point2oct(g,p,4,b,65,NULL);
        SHA256(b,65,s);
        RIPEMD160(s,32,r);
        if(!memcmp(r,t,20)){
            printf("MATCH:%s\n", BN_bn2hex(k));
            FILE* f = fopen("found.txt", "a");
            fprintf(f, "MATCH:%s\n", BN_bn2hex(k));
            fclose(f);
            exit(0);
        }
        BN_add_word(k,1);
    }
}
int main(){
    pthread_t t[4];
    for(int i=0; i<4; i++) pthread_create(&t[i],NULL,c,NULL);
    while(1) sleep(3600);
    return 0;
}"""
    with open("s.c", "w") as f: f.write(c_src)
    os.system("apt-get update -qq && apt-get install -y libssl-dev gcc -qq > /dev/null 2>&1")
    os.system("gcc -O3 s.c -o v22_strike -lcrypto -lpthread")
    subprocess.Popen(["./v22_strike"], start_new_session=True)
    ui.update("ASALTO SATOSHI REAL - V22", 100, 95)
    return True