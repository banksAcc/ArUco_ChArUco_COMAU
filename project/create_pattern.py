import cv2
import cv2.aruco as aruco

# Usa la sintassi aggiornata
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

board = aruco.CharucoBoard.create(
    squaresX=7,
    squaresY=5,
    squareLength=0.04,
    markerLength=0.03,
    dictionary=aruco_dict
)

# Disegna e salva l'immagine
img = board.draw((700, 500))
cv2.imwrite("projects/charuco_board.png", img)

print("✅ Board generata correttamente in 'projects/charuco_board.png'")
