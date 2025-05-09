import argparse
import datetime
import os

from calibration import run_calibration
from pose_estimation import run_pose_estimation

def log(message):
    """Salva log su file con timestamp"""
    with open("data/log.txt", "a") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {message}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sistema ChArUco")
    parser.add_argument(
        "--mode", choices=["calibra", "traccia"], required=True,
        help="Scegli 'calibra' per calibrazione, 'traccia' per tracking"
    )
    args = parser.parse_args()

    if args.mode == "calibra":
        print("🔧 Avvio calibrazione...")
        log("Avvio calibrazione")
        result = run_calibration()
        if result["success"]:
            print("✅ Calibrazione completata con successo.")
            log("Calibrazione completata con successo")
        else:
            print(f"❌ Errore durante la calibrazione: {result['error']}")
            log("Calibrazione in errore, ERROR: "+result['error'])
        
    elif args.mode == "traccia":
        print("🎯 Avvio tracking...")
        log("Avvio tracking")
        result = run_pose_estimation()

        if result["success"]:

            #File non esiste->creato. File esiste->sovrascritto
            with open("data/pose_log.txt", "w") as f:
                for i, (timestamp, x, y, z) in enumerate(result["poses"]):
                    f.write(f"Timestamp: {timestamp} - Frame {i+1}: x={x:.2f}, y={y:.2f}, z={z:.2f}\n")
            log("Tracking completato con successo")
        else:
            print(f"❌ Errore nel tracking: {result['error']}")
            log("Tracking completato in errore: ERROR: "+result['error'])
