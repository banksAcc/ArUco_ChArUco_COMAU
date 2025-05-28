import cv2
import cv2.aruco as aruco
import numpy as np
import os

def create_custom_charuco(board_size, square_length, marker_length, marker_ids, aruco_dict):
    board = aruco.CharucoBoard(board_size, square_length, marker_length, aruco_dict)

    # Sostituisce gli ID di default con quelli specificati
    board.ids = np.array(marker_ids, dtype=np.int32).reshape((board_size[1] - 1, board_size[0] - 1))
    return board

# Parametri board
board_size = (5, 5)  # quadrati
square_length = 15  # mm
marker_length = 10  # mm
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

# Genera due set di ID diversi
ids_board1 = list(range(0, 16))     # ID 0-15
ids_board2 = list(range(16, 32))    # ID 16-31

# Crea le due board
board1 = create_custom_charuco(board_size, square_length, marker_length, ids_board1, aruco_dict)
board2 = create_custom_charuco(board_size, square_length, marker_length, ids_board2, aruco_dict)

# Genera immagini
img1 = board1.generateImage((600, 600), marginSize=10, borderBits=1)
img2 = board2.generateImage((600, 600), marginSize=10, borderBits=1)

# Salva
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
os.makedirs(output_dir, exist_ok=True)

cv2.imwrite(os.path.join(output_dir, "charuco_board1.png"), img1)
cv2.imwrite(os.path.join(output_dir, "charuco_board2.png"), img2)

print("✅ Due ChArUco board diverse salvate come 'charuco_board1.png' e 'charuco_board2.png'")
