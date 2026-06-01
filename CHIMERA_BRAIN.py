# MISSION BRAIN V27.4 - SOCKS5H HARVEST Φ
import os, subprocess, time, requests, base64, socket, re, threading

def execute_mission(ui, ID):
    ui.log('Iniciando Mision V27.4 (SOCKS5H Native)...')
    try:
        # 1. Asegurar Tor
        os.system("pkill -9 tor; sleep 2; nohup tor > /dev/null 2>&1 &")
        time.sleep(30)
        
        # 2. Configurar Proxies
        proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        
        # 3. Cosecha
        queries = ["1Feex", "BTC", "Leak", "Database"]
        all_onions = []
        
        for q in queries:
            ui.log("Buscando en Ahmia: " + q)
            url = "http://juhanur2ik43jecy.onion/search/?q=" + q
            try:
                r = requests.get(url, proxies=proxies, timeout=60)
                if r.status_code == 200:
                    found = re.findall(r"[a-z2-7]{56}\.onion", r.text)
                    all_onions.extend(found)
                    ui.log("Encontrados " + str(len(found)) + " targets.")
            except Exception as e:
                ui.log("Error en query: " + str(e)[:30])
        
        unique_onions = list(set(all_onions))
        
        # 4. Reporte a Master C2 (Local)
        MASTER = "http://127.0.0.1:9471/"
        requests.post(MASTER, json={
            "node_id": ID, 
            "type": "TELEMETRY", 
            "payload": {"label": "BABEL_INDEX", "onions": unique_onions}
        }, timeout=10)
        
        ui.update("COSECHA V27.4 OK", 100, 5)
        ui.log("Indexados " + str(len(unique_onions)) + " targets.")
        
    except Exception as e:
        ui.log("Error V27.4: " + str(e))
    return True