import argparse
from calibration import run_calibration
from pose_estimation import run_pose_estimation

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sistema ChArUco Tracker")
    parser.add_argument("--mode", choices=["calibra", "traccia"], required=True, help="Modalità da eseguire")
    args = parser.parse_args()

    if args.mode == "calibra":
        run_calibration()
    elif args.mode == "traccia":
        run_pose_estimation()
