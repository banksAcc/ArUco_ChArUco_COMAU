import cv2
import numpy as np
import cv2.aruco as aruco
import time
import platform
import os

def run_calibration():
    """
    Esegue la calibrazione della fotocamera utilizzando una ChArUco board.

    Restituisce:
        dict: {"success": True, "error": None} se completata con successo,
              {"success": False, "error": <descrizione>} in caso di errore.

    Procedura:
    - Attiva la webcam.
    - Rileva marker ArUco e corner ChArUco.
    - Registra i corner validi da 30 frame diversi (o meno, se si preme 'q').
    - Calcola la matrice intrinseca della camera e i coefficienti di distorsione.
    - Salva i parametri in 'data/calib_data.npz'.

    Requisiti:
    - La board ChArUco deve essere visibile alla webcam in varie pose.
    - La libreria opencv-contrib-python deve essere installata.
    """

    try:
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
        board = aruco.CharucoBoard((12, 9), 30, 22, aruco_dict)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return {"success": False, "error": "Webcam non disponibile"}

        print("🎥 Webcam attiva. Premi 'q' per uscire.")
        print("📸 Acquisisci almeno 30 viste della board da angolazioni diverse.")

        all_corners = []
        all_ids = []
        valid_frames = 0
        image_size = None

        while True:
            ret, frame = cap.read()
            if not ret:
                return {"success": False, "error": "Errore nel leggere dalla webcam"}

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)

            if ids is not None and len(ids) > 0:
                aruco.drawDetectedMarkers(frame, corners, ids)
                retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
                    corners, ids, gray, board
                )

                if retval is not None and retval > 20:
                    all_corners.append(charuco_corners)
                    all_ids.append(charuco_ids)
                    valid_frames += 1
                    print(f"✅ Frame valido acquisito ({valid_frames}/30)")
                    print("🔄 Sposta la board in una nuova posizione...")

                    if platform.system() == "Windows":
                        import winsound
                        winsound.Beep(1000, 200)
                    else:
                        print('\a')

                    time.sleep(1.5)

                    if image_size is None:
                        image_size = gray.shape[::-1]

            cv2.imshow("Calibrazione ChArUco", frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or valid_frames >= 30:
                break

        cap.release()
        cv2.destroyAllWindows()

        if valid_frames < 5:
            return {"success": False, "error": "Pochi frame validi per la calibrazione"}

        print("⚙️ Calibrazione in corso...")

        rms, camera_matrix, dist_coeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
            charucoCorners=all_corners,
            charucoIds=all_ids,
            board=board,
            imageSize=image_size,
            cameraMatrix=None,
            distCoeffs=None
        )

        print(f"📏 Errore RMS della calibrazione: {rms:.4f}")
        print("📷 Matrice camera:")
        print(camera_matrix)
        print("📷 Coefficienti di distorsione:")
        print(dist_coeffs.ravel())

        os.makedirs("data", exist_ok=True)
        np.savez("data/calib_data.npz",
                 cameraMatrix=camera_matrix,
                 distCoeffs=dist_coeffs,
                 rvecs=rvecs,
                 tvecs=tvecs,
                 rms=rms)

        print("✅ Calibrazione completata. Parametri salvati in 'data/calib_data.npz'")
        return {"success": True, "error": None}

    except Exception as e:
        return {"success": False, "error": str(e)}
