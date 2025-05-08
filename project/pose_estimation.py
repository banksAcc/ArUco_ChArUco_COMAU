import cv2
import numpy as np
import cv2.aruco as aruco

def run_pose_estimation():
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    board = aruco.CharucoBoard_create(7, 5, 0.04, 0.03, aruco_dict)

    data = np.load("projects/calib_data.npz")
    cameraMatrix = data["cameraMatrix"]
    distCoeffs = data["distCoeffs"]

    cap = cv2.VideoCapture(0)
    print("Premi 'q' per uscire")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)
        if ids is not None and len(corners) > 0:
            retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, gray, board)
            if retval > 10:
                valid, rvec, tvec = aruco.estimatePoseCharucoBoard(
                    charuco_corners, charuco_ids, board, cameraMatrix, distCoeffs, None, None
                )
                if valid:
                    aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 0.05)

        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
