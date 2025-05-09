import cv2
import cv2.aruco as aruco

# Definizione del dizionario ArUco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Creazione della ChArUco board
board = aruco.CharucoBoard((7, 5), 0.04, 0.03, aruco_dict)

# Creazione dell'immagine della board
img = board.generateImage((700, 500), marginSize=10, borderBits=1)

# Salvataggio dell'immagine
cv2.imwrite("data/charuco_board.png", img)
print("✅ Board salvata come 'charuco_board.png'")
