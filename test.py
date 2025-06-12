import cv2
import numpy as np

# — Parametri board
board_size          = (5,5)       # 5×5 quadrati
square_length       = 0.04        # in metri
marker_length       = 0.03        # in metri
n_markers_per_board = (board_size[0]*board_size[1]) // 2  # =12

# — Dizionario unico
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_5X5_100
)

# — 1) Creo due board con ID diversi
ids1 = np.arange(0, n_markers_per_board, dtype=int)          # 0…11
ids2 = np.arange(n_markers_per_board, 2*n_markers_per_board, dtype=int)  # 12…23

# ATTENZIONE: in OpenCV 4.11 il costruttore CharucoBoard(...) ignora "ids",
# quindi per farli rispettare in Python devo usare la factory _create:
board1 = cv2.aruco.CharucoBoard(
    (board_size[0], board_size[1]),
    square_length, marker_length,
    ARUCO_DICT, ids1
)
board2 = cv2.aruco.CharucoBoard(
    (board_size[0], board_size[1]),
    square_length, marker_length,
    ARUCO_DICT, ids2
)

# — 2) Genero le due immagini e le concatena orizzontalmente
img1 = board1.generateImage((600,600))
img2 = board2.generateImage((600,600))
combined = np.hstack([img1, img2])

# — 3) Rilevo TUTTI i marker in un’unica passata
corners, ids, _ = cv2.aruco.detectMarkers(combined, ARUCO_DICT)
ids_flat = ids.flatten() if ids is not None else np.array([])

print("Detected raw IDs:", ids_flat)

# — 4) Filtri per i due gruppi
mask1 = ids_flat < n_markers_per_board          # marker 0…11
mask2 = (ids_flat >= n_markers_per_board) &      \
        (ids_flat < 2*n_markers_per_board)       # marker 12…23

corners1 = [corners[i] for i, ok in enumerate(mask1) if ok]
ids1_det = ids_flat[mask1].reshape(-1,1)

corners2 = [corners[i] for i, ok in enumerate(mask2) if ok]
ids2_det = ids_flat[mask2].reshape(-1,1)

# — 5) Ricostruisco i marker sul frame originale
vis1 = cv2.aruco.drawDetectedMarkers(combined.copy(), corners1, ids1_det, )
vis2 = cv2.aruco.drawDetectedMarkers(combined.copy(), corners2, ids2_det)

# — Mostro tutto
cv2.imshow("All Markers", combined)
cv2.imshow("Group 1 (IDs 0-11)", vis1)
cv2.imshow("Group 2 (IDs 12-23)", vis2)
cv2.waitKey(0)
cv2.destroyAllWindows()
