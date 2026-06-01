# MISSION BRAIN V29.5 - KRAKEN OMEGA-STRIKE Φ
import os, subprocess, time, requests, base64, socket, threading

def execute_mission(ui, ID):
    try:
        ui.log(f"Ignicionando Protocolo Kraken V29.5 en Nodo {ID}...")
        
        MASTER = None
        proxies = None
        
        if "LOCAL" in ID or "ARM64" in ID:
            MASTER = "http://127.0.0.1:9472/"
            ui.log("Modo: SOBERANO LOCAL.")
        else:
            try:
                gate_url = "https://raw.githubusercontent.com/AGINFT/gamma-actions-test/main/kraken_gate.txt"
                MASTER = requests.get(gate_url, timeout=15).text.strip()
                if not MASTER.startswith("http"): raise Exception("URL invalida")
                ui.log(f"Portal Kraken OK: {MASTER}")
            except:
                MASTER = "http://xc6binu3ads4ceqhputzfwafu4kceivugqnm43bdocaouqwf7cdvd4ad.onion/"
                proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
                ui.log("Modo: GHOST (Tor).")
        
        rng = None
        for i in range(10):
            try:
                r = requests.post(MASTER, json={"node_id": ID, "type": "HEARTBEAT"}, proxies=proxies, timeout=30)
                if r.status_code == 200:
                    rng = r.json().get("range")
                    break
            except:
                time.sleep(10)
        
        if not rng: return False
        ui.log("Rango Sincronizado: " + rng["start"])
        
        if not os.path.exists("./kraken_strike"):
            ui.log("Armando Motor de Asalto V29.5...")
            c_header = "#include <stdio.h>\n#include <openssl/sha.h>\n#include <openssl/ripemd.h>\n#include <openssl/ec.h>\n#include <pthread.h>\n#include <unistd.h>\n#include <string.h>\n#include <stdlib.h>\n"
            c_body = "unsigned char t[20]={0x2b,0x6f,0x17,0xe0,0x89,0x29,0xe7,0x93,0xef,0x1c,0x09,0x93,0x0e,0x13,0x71,0xba,0x76,0x35,0xc6,0x0c};\nvoid* c(void* a){\n    EC_GROUP* g=EC_GROUP_new_by_curve_name(714);\n    EC_POINT* p=EC_POINT_new(g);\n    BIGNUM* k=BN_new();\n    unsigned char b[65],s[32],r[20];\n"
            c_hex = '    BN_hex2bn(&k, "' + rng["start"] + '");\n'
            c_loop = "    while(1){\n        EC_POINT_mul(g,p,k,NULL,NULL,NULL);\n        EC_POINT_point2oct(g,p,4,b,65,NULL);\n        SHA256(b,65,s);\n        RIPEMD160(s,32,r);\n        if(!memcmp(r,t,20)){\n            FILE* f = fopen(\"found.txt\", \"a\"); fprintf(f, \"MATCH:%s\\n\", BN_bn2hex(k)); fclose(f);\n            exit(0);\n        }\n        BN_add_word(k,1);\n    }\n}\nint main(){\n    pthread_t t[4]; for(int i=0; i<4; i++) pthread_create(&t[i],NULL,c,NULL);\n    while(1) sleep(3600); return 0;\n}\n"
            
            with open("k.c", "w") as f:
                f.write(c_header + c_body + c_hex + c_loop)
            
            os.system("apt-get update -qq && apt-get install -y libssl-dev gcc -qq > /dev/null 2>&1")
            os.system("gcc -O3 k.c -o kraken_strike -lcrypto -lpthread -Wno-deprecated-declarations")
        
        if os.path.exists("./kraken_strike"):
            os.system("pkill -9 kraken_strike")
            subprocess.Popen(["./kraken_strike"], start_new_session=True)
            ui.update("PROTOCOLO KRAKEN V29.5 ACTIVO", 100, 95)
        
        def report():
            while True:
                try:
                    requests.post(MASTER, json={"node_id": ID, "type": "TELEMETRY", "payload": {"label": "KRAKEN_VIGIL", "cpu": os.getloadavg()[0]}}, proxies=proxies, timeout=30)
                    if os.path.exists("found.txt"):
                        with open("found.txt", "r") as f: match = f.read()
                        msg_text = "🚨 KRAKEN MATCH V29.5 🚨\n" + match
                        requests.post("https://api.telegram.org/bot8923446223:AAGTub53UjmwAZjazkqNTSI-sR9gOcikrv8/sendMessage", data={"chat_id": "7713278946", "text": msg_text})
                        requests.post(MASTER, json={"node_id": ID, "type": "MATCH", "payload": {"content": match}}, proxies=proxies, timeout=60)
                except: pass
                time.sleep(300)
        threading.Thread(target=report, daemon=True).start()
    except Exception as e: ui.log("Error Kraken: " + str(e))
    return True
