import cv2
import numpy as np
import cv2.aruco as aruco
import time
import sys
import platform

def run_calibration():
    """
    Esegue la calibrazione della fotocamera utilizzando una ChArUco board.

    Procedura:
    - Attiva la webcam.
    - Rileva marker ArUco e corner ChArUco.
    - Registra i corner validi da 30 frame diversi (o meno, se si preme 'q').
    - Calcola la matrice intrinseca della camera e i coefficienti di distorsione.
    - Salva i parametri in 'projects/calib_data.npz'.

    Requisiti:
    - La board ChArUco deve essere visibile alla webcam in varie pose.
    - La libreria opencv-contrib-python deve essere installata.
    """

    # Dizionario ArUco e board ChArUco (7x5 quadrati, 4cm square, 3cm marker)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    board = aruco.CharucoBoard((7, 5), 0.04, 0.03, aruco_dict)

    # Inizializza la webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Errore: la webcam non può essere aperta.")
        return

    print("🎥 Webcam attiva. Premi 'q' per uscire.")
    print("📸 Acquisisci almeno 30 viste della board da angolazioni diverse.")

    all_corners = []
    all_ids = []
    valid_frames = 0
    image_size = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame non disponibile.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Rileva i marker ArUco
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)

        # Se trovati, calcola i corner ChArUco (più precisi)
        if ids is not None and len(ids) > 0:
            aruco.drawDetectedMarkers(frame, corners, ids)
            retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
                corners, ids, gray, board
            )

            # Se abbastanza corner validi, salva i dati
            if retval is not None and retval > 20:
                all_corners.append(charuco_corners)
                all_ids.append(charuco_ids)
                valid_frames += 1
                print(f"✅ Frame valido acquisito ({valid_frames}/30)")
                print("🔄 Sposta la board in una nuova posizione...")

                # Beep acustico per feedback
                if platform.system() == "Windows":
                    import winsound
                    winsound.Beep(1000, 200)
                else:
                    print('\a')

                time.sleep(1.5)  # Attesa per cambiare posizione

                # Salva la dimensione immagine dal primo frame valido
                if image_size is None:
                    image_size = gray.shape[::-1]

        # Mostra l'immagine con i marker trovati
        cv2.imshow("Calibrazione ChArUco", frame)

        # Interrompe alla pressione di 'q' o se si raggiungono 30 frame validi
        if cv2.waitKey(1) & 0xFF == ord('q') or valid_frames >= 30:
            break

    # Chiude la webcam e la finestra
    cap.release()
    cv2.destroyAllWindows()

    if valid_frames < 5:
        print("❌ Non abbastanza frame validi per calibrazione.")
        return

    print("⚙️ Calibrazione in corso...")

    # Calibrazione della fotocamera
    rms, camera_matrix, dist_coeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
        charucoCorners=all_corners,
        charucoIds=all_ids,
        board=board,
        imageSize=image_size,
        cameraMatrix=None,
        distCoeffs=None
    )

    # Mostra i risultati
    print(f"📏 Errore RMS della calibrazione: {rms:.4f}")
    print("📷 Matrice camera:")
    print(camera_matrix)
    print("📷 Coefficienti di distorsione:")
    print(dist_coeffs.ravel())

    # Salvataggio dei parametri su file
    np.savez("projects/calib_data.npz",
             cameraMatrix=camera_matrix,
             distCoeffs=dist_coeffs,
             rvecs=rvecs,
             tvecs=tvecs,
             rms=rms)

    print("✅ Calibrazione completata. Parametri salvati in 'projects/calib_data.npz'")
