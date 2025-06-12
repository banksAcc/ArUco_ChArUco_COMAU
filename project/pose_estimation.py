import cv2
import numpy as np
import os
import cv2.aruco as aruco
from datetime import datetime

def run_pose_estimation():
    """
    Esegue la stima della posa (pose estimation) in tempo reale di una ChArUco board
    utilizzando una webcam, sulla base di parametri precedentemente calibrati.

    Requisiti:
    - Deve esistere il file 'data/calib_data.npz' contenente:
        - cameraMatrix
        - distCoeffs
    - La board ChArUco deve essere visibile alla webcam.

    Restituisce:
        dict: {
            "success": True/False,
            "error": <messaggio> (solo in caso di errore)
        }
    """
    try:
        # Verifica presenza parametri di calibrazione
        if not os.path.exists("data/calib_data.npz"):
            return {"success": False, "error": "File calib_data.npz non trovato."}

        # OpenCV 4.11 compat: usa getPredefinedDictionary
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
        # board = aruco.CharucoBoard((7, 5), 0.04, 0.03, aruco_dict)
        board = aruco.CharucoBoard((5, 5), 0.04, 0.03, aruco_dict)


        # Carica parametri camera
        data = np.load("data/calib_data.npz")
        cameraMatrix = data["cameraMatrix"]
        distCoeffs = data["distCoeffs"]

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return {"success": False, "error": "Webcam non disponibile"}

        print("🎯 Tracking attivo. Premi 'q' per uscire.")
        poses = []  # raccoglie (x, y, z) delle pose valide
        valid_frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                return {"success": False, "error": "Impossibile leggere dalla webcam"}

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)

            if ids is not None and len(corners) > 0:
                retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
                    corners, ids, gray, board
                )

                if retval and retval > 10:
                    valid, rvec, tvec = aruco.estimatePoseCharucoBoard(
                        charuco_corners, charuco_ids, board,
                        cameraMatrix, distCoeffs, None, None
                    )
                    if valid:
                        cv2.drawFrameAxes(frame, cameraMatrix, distCoeffs, rvec, tvec, 0.05)

                        valid_frame_count += 1

                        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # es. 14:52:03.123
                        x, y, z = tvec.flatten()                        
                        poses.append((timestamp, x, y, z))
                        
                        # Estrai coordinate XYZ e stampa
                        if valid_frame_count % 10 == 0:
                            print(f"Posizione marker (XYZ): {x:.2f}, {y:.2f}, {z:.2f}")
                            
            # Origine nel mondo
            origin_point = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

            # Calcola dove si proietta sull'immagine
            image_points, _ = cv2.projectPoints(
                origin_point,  # punto 3D
                np.zeros((3, 1)),  # rotazione = 0
                np.zeros((3, 1)),  # traslazione = 0
                cameraMatrix,
                distCoeffs
            )

            # Disegna sul frame
            x, y = image_points[0][0]
            cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
            cv2.putText(frame, "O", (int(x)+10, int(y)-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            cv2.imshow("Tracking ChArUco", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return {"success": True, "error": None, "poses": poses}

    except Exception as e:
        return {"success": False, "error": str(e)}
