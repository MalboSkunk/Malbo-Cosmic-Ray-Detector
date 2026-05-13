from dotenv import load_dotenv
import cv2
import numpy as np
import time
import os
import json
import requests  # Pour Discord
from datetime import datetime

load_dotenv()


# --- RÉGLAGES ---
SEUIL = 32 
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK") # À créer dans les paramètres de ton salon Discord
STATION_ID = "Malbo_Vailly_Station_01"

main_folder = "/home/pi/malbot/Captures_Muons"
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

# --- FONCTION D'ENVOI DISCORD & LOG SCIENTIFIQUE ---
def log_and_notify(file_path, pixel_count, type_muon):
    now = datetime.now()
    timestamp_utc = datetime.utcnow().isoformat()
    
    # 1. Création du Log JSON pour CREDO
    log_data = {
        "device_id": STATION_ID,
        "timestamp": timestamp_utc,
        "type": type_muon,
        "pixels": int(pixel_count),
        "location": "Vailly-sur-Aisne",
        "sensor": "CMOS_Logitech_Mod"
    }
    
    json_path = file_path.replace(".png", ".json")
    with open(json_path, 'w') as f:
        json.dump(log_data, f, indent=4)

    # 2. Envoi vers Discord (Image + Infos)
    try:
        with open(file_path, 'rb') as f:
            payload = {'content': f"🚨 **{type_muon.upper()} DÉTECTÉ !**\n📍 Station : {STATION_ID}\n🔥 Intensité : {pixel_count} pixels"}
            requests.post(WEBHOOK_URL, data=payload, files={'file': f}, timeout=5)
    except Exception as e:
        print(f"Erreur d'envoi Discord : {e}")

# --- INITIALISATION CAMÉRA ---
cap = cv2.VideoCapture(0)
count = 0

print("Chasse H24 lancée sur le Raspberry Pi... Alerte Discord active !")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, SEUIL, 255, cv2.THRESH_BINARY)
        pixel_count = np.sum(thresh == 255)

        if pixel_count > 0:
            count += 1
            date_now = datetime.now()
            date_formattee = date_now.strftime("%d-%m-%Y_%Hh%M_%Ss")
            
            type_muon = "muon_trait" if pixel_count > 4 else "muon_point"
            file_name = f"{type_muon}_{date_formattee}.png"
            file_path = os.path.join(main_folder, file_name)
            
            cv2.imwrite(file_path, frame)
            
            # --- APPEL DE L'AUTOMATISATION ---
            log_and_notify(file_path, pixel_count, type_muon)
            
            print(f"IMPACT ! Fichier: {file_name} (Notif envoyée)")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nArrêt manuel.")
finally:
    cap.release()