import cv2
import cv2.aruco as aruco
import os

# Definizione del dizionario ArUco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Creazione della ChArUco board
board = aruco.CharucoBoard((7, 5), 0.04, 0.03, aruco_dict)

# Creazione dell'immagine della board
img = board.generateImage((700, 500), marginSize=10, borderBits=1)


output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
os.makedirs(output_dir, exist_ok=True)  # crea ../data se non esiste

output_path = os.path.join(output_dir, "charuco_board.png")
cv2.imwrite(output_path, img)

print("✅ Board salvata come 'charuco_board.png'")
