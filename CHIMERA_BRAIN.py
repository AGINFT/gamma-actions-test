# MISSION BRAIN V27.5 - OMNI HARVEST Φ
import os, subprocess, time, requests, base64, socket, re, threading

def execute_mission(ui, ID):
    ui.log('Iniciando Mision V27.5 (Omni-Harvest)...')
    try:
        proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        engines = [
            "http://juhanur2ik43jecy.onion/search/?q=",
            "http://haystak24p7um6af.onion/?q=",
            "http://torchde76266ny67.onion/search?query="
        ]
        
        queries = ["1Feex", "BTC", "Leak"]
        all_onions = []
        
        for engine in engines:
            for q in queries:
                ui.log("Consultando: " + engine.split("//")[1][:10] + "... para " + q)
                try:
                    r = requests.get(engine + q, proxies=proxies, timeout=45)
                    if r.status_code == 200:
                        found = re.findall(r"[a-z2-7]{56}\.onion", r.text)
                        all_onions.extend(found)
                        ui.log("Encontrados " + str(len(found)) + " targets.")
                except: pass
        
        unique_onions = list(set(all_onions))
        MASTER = "http://127.0.0.1:9471/"
        requests.post(MASTER, json={
            "node_id": ID, 
            "type": "TELEMETRY", 
            "payload": {"label": "BABEL_INDEX", "onions": unique_onions}
        }, timeout=10)
        
        ui.update("COSECHA V27.5 OK", 100, 5)
        ui.log("Cosecha finalizada. Total: " + str(len(unique_onions)))
        
    except Exception as e:
        ui.log("Error V27.5: " + str(e))
    return True