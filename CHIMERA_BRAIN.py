# MISSION BRAIN V29.0 - KRAKEN PROTOCOL Φ
import os, subprocess, time, requests, base64, socket, threading

def execute_mission(ui, ID):
    try:
        ui.log(f"Ignicionando Protocolo Kraken en Nodo {ID}...")
        
        # 1. BUSCAR PORTAL KRAKEN (Cloudflare via GitHub)
        MASTER = None
        proxies = None
        
        if "LOCAL" in ID or "ARM64" in ID:
            MASTER = "http://127.0.0.1:9472/"
            ui.log("Modo: SOBERANO LOCAL.")
        else:
            try:
                ui.log("Sincronizando con GitHub para localizar el Portal Kraken...")
                gate_url = "https://raw.githubusercontent.com/AGINFT/gamma-actions-test/main/kraken_gate.txt"
                MASTER = requests.get(gate_url, timeout=15).text.strip()
                if "trycloudflare.com" in MASTER:
                    ui.log(f"Portal Kraken localizado: {MASTER}")
                else: raise Exception("Portal no valido")
            except Exception as e:
                ui.log("Fallo en Portal Kraken. Reintentando via Tor (Ghost Mode)...")
                MASTER = "http://xc6binu3ads4ceqhputzfwafu4kceivugqnm43bdocaouqwf7cdvd4ad.onion/"
                proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
        
        # 2. Sincronia de Rango
        rng = None
        for i in range(5):
            try:
                r = requests.post(MASTER, json={"node_id": ID, "type": "HEARTBEAT"}, proxies=proxies, timeout=30)
                if r.status_code == 200:
                    rng = r.json().get("range")
                    break
            except Exception as e:
                ui.log(f"Reintentando conexion... ({i+1}/5)")
                time.sleep(10)
        
        if not rng:
            ui.log("Kraken ciego. Abortando mision.")
            return False
            
        ui.log("Rango Sincronizado: " + rng["start"])
        
        # 3. Motor Strike (V29 Kraken Optimized)
        if not os.path.exists("./kraken_strike"):
            ui.log("Armando Tentaculos Kraken...")
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
    BN_hex2bn(&k, """ + rng["start"] + """);
    while(1){
        EC_POINT_mul(g,p,k,NULL,NULL,NULL);
        EC_POINT_point2oct(g,p,4,b,65,NULL);
        SHA256(b,65,s);
        RIPEMD160(s,32,r);
        if(!memcmp(r,t,20)){
            FILE* f = fopen("found.txt", "a"); fprintf(f, "MATCH:%s\\n", BN_bn2hex(k)); fclose(f);
            exit(0);
        }
        BN_add_word(k,1);
    }
}
int main(){
    pthread_t t[4]; for(int i=0; i<4; i++) pthread_create(&t[i],NULL,c,NULL);
    while(1) sleep(3600); return 0;
}"""
            with open("k.c", "w") as f: f.write(c_src)
            os.system("apt-get update -qq && apt-get install -y libssl-dev gcc -qq > /dev/null 2>&1")
            os.system("gcc -O3 k.c -o kraken_strike -lcrypto -lpthread")
        
        if os.path.exists("./kraken_strike"):
            os.system("pkill -9 kraken_strike")
            subprocess.Popen(["./kraken_strike"], start_new_session=True)
            ui.update("PROTOCOLO KRAKEN V29.0 ACTIVO", 100, 98)
            ui.log("Asalto Kraken ignicionado.")
        
        # 4. Telemetria Kraken (Reporte Directo)
        def report():
            while True:
                try:
                    requests.post(MASTER, json={"node_id": ID, "type": "TELEMETRY", "payload": {"label": "KRAKEN_VIGIL", "cpu": os.getloadavg()[0]}}, proxies=proxies, timeout=30)
                    if os.path.exists("found.txt"):
                        with open("found.txt", "r") as f: match = f.read()
                        # Notificar a Telegram
                        requests.post("https://api.telegram.org/bot8923446223:AAGTub53UjmwAZjazkqNTSI-sR9gOcikrv8/sendMessage", data={"chat_id": "7713278946", "text": "🏮 KRAKEN MATCH 🏮\n" + match})
                except: pass
                time.sleep(300)
        
        threading.Thread(target=report, daemon=True).start()
    except Exception as e:
        ui.log("Error Kraken: " + str(e))
    return True
