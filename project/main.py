import argparse
import datetime
import os

from calibration import run_calibration
from pose_estimation import run_pose_estimation

def log(message):
    """Salva log su file con timestamp"""
    with open("log.txt", "a") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {message}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sistema ChArUco")
    parser.add_argument(
        "--mode", choices=["calibra", "traccia"], required=True,
        help="Scegli 'calibra' per calibrazione, 'traccia' per tracking"
    )
    args = parser.parse_args()

    os.makedirs("projects", exist_ok=True)

    if args.mode == "calibra":
        print("🔧 Avvio calibrazione...")
        log("Avvio calibrazione")
        run_calibration()
        log("Calibrazione completata")
    elif args.mode == "traccia":
        print("🎯 Avvio tracking...")
        log("Avvio tracking")
        run_pose_estimation()
        log("Tracking completato")
