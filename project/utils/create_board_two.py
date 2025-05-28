import cv2
import cv2.aruco as aruco
import os

# Parametri board
square_length = 0.04  # mm (per calibrazione, non influisce sul PNG)
marker_length = 0.03  # mm
board_size = (5, 5)
image_size = (885, 885)  # per 75 mm a 300 DPI

# Dizionari diversi
dict1 = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
dict2 = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Boards
board1 = aruco.CharucoBoard(board_size, square_length, marker_length, dict1)
board2 = aruco.CharucoBoard(board_size, square_length, marker_length, dict2)

# Generazione immagini
img1 = board1.generateImage(image_size)
img2 = board2.generateImage(image_size)

# Salvataggio
output_dir = os.path.abspath("./charuco_output")
os.makedirs(output_dir, exist_ok=True)

cv2.imwrite(os.path.join(output_dir, "charuco_board1.png"), img1)
cv2.imwrite(os.path.join(output_dir, "charuco_board2.png"), img2)

print("✅ Immagini salvate in ./charuco_output/ — pronte per stampa a 75×75mm @ 300 DPI")
