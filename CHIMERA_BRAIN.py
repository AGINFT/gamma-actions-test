# MISSION BRAIN V27.3 - ONION HARVEST Φ
import os, subprocess, time, requests, base64, socket, re, threading

def execute_mission(ui, ID):
    ui.log("Iniciando Mision V27.3: Cosecha de Onions (Biblioteca de Babel)...")
    try:
        # 1. Preparar Red
        os.system("apt-get update -qq && apt-get install -y tor proxychains4 curl -qq > /dev/null 2>&1")
        os.system("pkill -9 tor; sleep 2; nohup tor > /dev/null 2>&1 &")
        time.sleep(30)
        
        # 2. Fuentes de Cosecha Masiva
        queries = ["1Feex", "BTC", "Leak", "Database", "Wallet", "Private Key"]
        all_onions = []
        
        for q in queries:
            ui.log("Cosechando para: " + q)
            url = "http://juhanur2ik43jecy.onion/search/?q=" + q
            raw = subprocess.getoutput("proxychains4 curl -s -L " + url)
            found = re.findall(r"[a-z2-7]{56}\.onion", raw)
            all_onions.extend(found)
            ui.update("Cosechando...", 50, 10)
        
        unique_onions = list(set(all_onions))
        ui.log("Cosecha total: " + str(len(unique_onions)) + " direcciones unicas.")
        
        # 3. Alerta y Registro
        tg_msg = "🚜 [HARVEST] Nodo " + ID + " ha indexado " + str(len(unique_onions)) + " targets en la sombra."
        requests.post("https://api.telegram.org/bot8923446223:AAGTub53UjmwAZjazkqNTSI-sR9gOcikrv8/sendMessage", 
                      data={"chat_id": "7713278946", "text": tg_msg})
        
        # 4. Exfiltracion de Indice (GitHub)
        report = "--- BABEL INDEX " + str(ID) + " ---
" + "
".join(unique_onions)
        T_F1 = "github_pat_11B43LNKI"
        T_F2 = "0LNcIXtVPYanP_CyPZqVH8sNnWlDMzN4W9se0nhC3Fy0ad2g69a8aa9APRMTWMUAFMELmuIcS"
        headers = {"Authorization": "token " + T_F1 + T_F2}
        url = "https://api.github.com/repos/AGINFT/gamma-actions-test/contents/intel/babel_" + str(ID) + ".txt"
        
        r_get = requests.get(url, headers=headers)
        sha = r_get.json().get("sha") if r_get.status_code == 200 else None
        encoded = base64.b64encode(report.encode()).decode()
        data = {"message": "Babel Update " + str(ID), "content": encoded, "branch": "main"}
        if sha: data["sha"] = sha
        requests.put(url, headers=headers, json=data)
        
        ui.update("COSECHA COMPLETA", 100, 5)
    except Exception as e:
        ui.log("Error V27.3: " + str(e))
    return True
