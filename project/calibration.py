import cv2
import numpy as np
import cv2.aruco as aruco

def run_calibration():
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    board = aruco.CharucoBoard_create(7, 5, 0.04, 0.03, aruco_dict)

    cap = cv2.VideoCapture(0)
    all_corners, all_ids = [], []
    counter = 0

    print("Premi 'q' per terminare o attendi 30 acquisizioni valide.")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)
        if len(corners) > 0:
            retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, gray, board)
            if retval > 20:
                all_corners.append(charuco_corners)
                all_ids.append(charuco_ids)
                counter += 1
                print(f"Frame validi acquisiti: {counter}")

        cv2.imshow('Calibrazione', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or counter >= 30:
            break

    cap.release()
    cv2.destroyAllWindows()

    ret, cameraMatrix, distCoeffs, _, _ = aruco.calibrateCameraCharuco(
        charucoCorners=all_corners,
        charucoIds=all_ids,
        board=board,
        imageSize=gray.shape[::-1],
        cameraMatrix=None,
        distCoeffs=None
    )

    np.savez("projects/calib_data.npz", cameraMatrix=cameraMatrix, distCoeffs=distCoeffs)
    print("✅ Calibrazione completata e salvata in 'calib_data.npz'")
