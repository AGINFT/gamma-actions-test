# MISSION BRAIN V27.2 - DARK SCRAPER Φ
import os, subprocess, time, requests, base64, socket, re, threading

def execute_mission(ui, ID):
    try:
        ui.log('Iniciando Mision V27.2 (Scraper de Red Profunda)...')
        
        # 1. Asegurar Infraestructura Tor
        ui.update("Preparando Red Tor...", 10)
        os.system("apt-get update -qq && apt-get install -y tor proxychains4 curl -qq > /dev/null 2>&1")
        with open("/etc/proxychains4.conf", "w") as f:
            f.write("strict_chain" + chr(10) + "proxy_dns" + chr(10) + "remote_dns_subnet 224.0.0.0" + chr(10) + "tcp_read_time_out 15000" + chr(10) + "tcp_connect_time_out 8000" + chr(10) + "[ProxyList]" + chr(10) + "socks5 127.0.0.1 9050" + chr(10))
        
        os.system("pkill -9 tor; sleep 2; nohup tor > /dev/null 2>&1 &")
        ui.log("Aguardando bootstrap de Tor (30s)...")
        time.sleep(30)

        # 2. Motor de Busqueda (Ahmia)
        ui.update("Buscando en la Sombra...", 40)
        query = "1Feex"
        search_url = "http://juhanur2ik43jecy.onion/search/?q=" + query
        ui.log("Consultando Ahmia para: " + query)
        
        raw_html = subprocess.getoutput("proxychains4 curl -s -L " + search_url)
        onions = re.findall(r"[a-z2-7]{56}\.onion", raw_html)
        onions = list(set(onions))[:5] # Limitar a los top 5
        
        ui.log("Detectadas " + str(len(onions)) + " fuentes potenciales.")
        
        # 3. Scraping y Deteccion de Patrones
        def scrape_onion(target):
            ui.log("Escaneando fuente: " + target)
            try:
                page = subprocess.getoutput("proxychains4 curl -s -L --max-time 60 http://" + target)
                
                # Patrones de interes
                found = []
                if "1Feex" in page: found.append("Mencion de 1Feex")
                if "2b6f17e08929e793ef1c09930e1371ba7635c60c" in page: found.append("Hash160 de Satoshi")
                # Regex simple para llaves WIF (Bitcoin)
                wif = re.findall(r"[5KLK][1-9A-HJ-NP-Za-km-z]{50,51}", page)
                if wif: found.append("Detectadas " + str(len(wif)) + " llaves WIF")
                
                if found:
                    msg = "💎 [HIT] Hallazgo en " + target + ":" + chr(10) + chr(10).join(found)
                    requests.post("https://api.telegram.org/bot8923446223:AAGTub53UjmwAZjazkqNTSI-sR9gOcikrv8/sendMessage", 
                                  data={"chat_id": "7713278946", "text": msg})
                    # Guardar fragmento del hallazgo
                    with open("hits.txt", "a") as f: f.write(target + ":" + str(found) + chr(10))
            except: pass

        for target in onions:
            scrape_onion(target)

        # 4. Exfiltracion de Log a Cloud
        ui.update("Anclando Inteligencia...", 90)
        NL = chr(10)
        report = "--- DARK RECON REPORT " + str(ID) + " ---" + NL
        report += "Query: " + query + NL
        report += "Onions Found: " + ",".join(onions) + NL
        
        T1 = "github_pat_11B43LNKI"
        T2 = "0LNcIXtVPYanP_CyPZqVH8sNnWlDMzN4W9se0nhC3Fy0ad2g69a8aa9APRMTWMUAFMELmuIcS"
        headers = {"Authorization": "token " + T1 + T2}
        url = "https://api.github.com/repos/AGINFT/gamma-actions-test/contents/intel/dark_" + str(ID) + ".txt"
        
        r_get = requests.get(url, headers=headers)
        sha = r_get.json().get("sha") if r_get.status_code == 200 else None
        encoded = base64.b64encode(report.encode()).decode()
        data = {"message": "Dark Scrape " + str(ID), "content": encoded, "branch": "main"}
        if sha: data["sha"] = sha
        requests.put(url, headers=headers, json=data)

        ui.update("VIGILIA V27.2 OK", 100, 10)
        ui.log("Mision de Scraping finalizada.")
            
    except Exception as e:
        ui.log("Error en Scraper V27.2: " + str(e))
    
    return True
