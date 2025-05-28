import cv2
import cv2.aruco as aruco
import numpy as np
import os
import math

# — Parametri di base per la Charuco board e l’immagine di output
board_size    = (5, 5)       # numero di quadrati in X e Y (5×5)
square_length = 0.04         # lato di ogni quadrato in metri (usato solo per calibrazione)
marker_length = 0.03         # lato di ogni marker ArUco in metri
image_size    = (885, 885)   # dimensione dell’immagine finale in pixel (75 mm @300 DPI → 885 px)
dictionary    = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
                             # dizionario di marker 5×5 con 100 possibili ID

# — Calcolo “a mano” quanti marker serviranno
squares_x, squares_y = board_size
# ArUco posiziona marker solo sulle caselle bianche di una scacchiera 5×5:
# in totale floor(25/2) = 12 marker
n_markers = (squares_x * squares_y) // 2  # = 12

# — Creo due liste di ID distinti, entrambe della lunghezza esatta n_markers
# ids1 = [0, 1, 2, …, 11]
ids1 = np.arange(0, n_markers, dtype=int)
# ids2 = [12, 13, 14, …, 23]
ids2 = np.arange(n_markers, 2 * n_markers, dtype=int)

# — Creo la prima Charuco board passando gli ID ids1
board1 = aruco.CharucoBoard(
    board_size,      # dimensione (tupla)
    square_length,   # lunghezza quadrati
    marker_length,   # lunghezza marker
    dictionary,      # dizionario ArUco
    ids1             # lista degli ID da usare
)

# — Creo la seconda board con gli stessi parametri ma ID diversi (ids2)
board2 = aruco.CharucoBoard(
    board_size,
    square_length,
    marker_length,
    dictionary,
    ids2
)

# — Generazione delle immagini PNG delle due board
img1 = board1.generateImage(image_size)
img2 = board2.generateImage(image_size)

# — Preparazione della cartella di output
output_dir = os.path.abspath("./charuco_output")
os.makedirs(output_dir, exist_ok=True)

# — Salvataggio su disco dei due file
cv2.imwrite(os.path.join(output_dir, "charuco_board1.png"), img1)
cv2.imwrite(os.path.join(output_dir, "charuco_board2.png"), img2)

print("✅ Immagini salvate in ./charuco_output/ — due board con lo stesso dizionario ma pattern diversi")
