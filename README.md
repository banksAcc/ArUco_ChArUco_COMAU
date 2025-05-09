# Sistema di Rilevamento Posizione con ArUco/ChArUco

Questo progetto implementa un sistema di **calibrazione della fotocamera** e **stima della posa** usando marker **ArUco** e **ChArUco**, sfruttando `OpenCV 4.11` con `opencv-contrib-python`. Il progetto è pensato per applicazioni di visione artificiale, robotica, tracking spaziale e realtà aumentata.

## 🔧 Funzionalità principali

- 📸 **Calibrazione della fotocamera** con board ChArUco (combinazione scacchiera + marker ArUco)
- 🎯 **Tracking in tempo reale** della board e stima della posa 3D (`x, y, z`)
- 🗂 **Logging automatico** dei dati di tracking, inclusi timestamp e coordinate
- 🔊 Feedback visivo/acustico per l'utente durante la calibrazione
- 📁 Salvataggio dati:
  - Parametri di calibrazione (`cameraMatrix`, `distCoeffs`, etc.)
  - Posizioni rilevate in tracking (`pose_log.txt`)
  - Log generale delle operazioni (`log.txt`)

## 🚀 Come usare

Assicurati di avere la board `charuco_board.png` generata e visibile alla webcam (stampata o su schermo). Nel caso non abbiate la board usate lo scritp utils/create_board.py per generarla, salvera il file in ../data/charuco_board.png

### ▶️ Avvio

Apri terminale nella cartella `project`:

```bash
# Calibrazione fotocamera
python main.py --mode calibra

# Tracking della board e stima posa
python main.py --mode traccia
```

Chiaramente la prima fase è di calibrazione, in cui calibriamo la camera del nostro device andando a creare il file calib_data.npz nella cartella data. Successivamente possiamo utilizzare la funzione di stima posa.

## 📂 Struttura del progetto

```
project/
├── calibration.py           # Calibrazione fotocamera con ChArUco
├── pose_estimation.py       # Tracking e stima posa
├── main.py                  # Entry point principale
├── requirements.txt         # Dipendenze
├── utils/
│   └── create_board.py      # Generazione immagine ChArUco
├── data/
│   ├── calib_data.npz       # File parametri camera
│   ├── charuco_board.png    # Immagine ChArUco da stampare
│   ├── pose_log.txt         # Log coordinate pose stimate
│   └── log.txt              # Log delle operazioni eseguite
```

## 🧪 Requisiti

Installa le dipendenze con:

```bash
pip install -r requirements.txt
```

Assicurati di avere **opencv-contrib-python ≥ 4.11.0** (preferibile versione 4.11, ultima ver. stabile al momento 09/05/25)

## 📏 Formato dei dati di tracking

Ogni riga di `pose_log.txt` contiene:

```
Timestamp: <sec.unix> - Frame <n>: x=<X>, y=<Y>, z=<Z>
```

Coordinate espresse nell'unità scelta nella definizione della board (es. metri o centimetri). Noi stiamo usando i metri.

## 💬 Note aggiuntive

- L'origine `(0,0,0)` della camera è rappresentata simbolicamente nel frame con un punto/etichetta di colore verde. Chiaramente non è possibile definire il punto Z = 0 sul piano immagine, quindi si tratta di una rappresentazione indicativa.
- Il sistema salva automaticamente tutti i file in `project/data/`.
- Tutte le eccezioni vengono catturate e ritornate in modo loggabile dal main.
- Nella cartella `images/` potete trovare alcune immagini in riferimento alle varie fasi di progettazione e sviluppo.
- Se usate uno smartphone per mostrare il marker e siete al buio/di sera, mettete al minimo la luminosità per massimizzare la visibilità alla camera del PC.
- La documentazione di riferimento è consultabile qui:
  - [📚 OpenCV ArUco Module](https://docs.opencv.org/4.11.0/d9/d6a/group__aruco.html)
  - [📏 Camera Calibration Tutorial (chessboard)](https://docs.opencv.org/4.11.0/dc/dbb/tutorial_py_calibration.html)
  - [📌 cv::aruco::CharucoBoard](https://docs.opencv.org/4.11.0/d0/d3c/classcv_1_1aruco_1_1CharucoBoard.html)
  - [📌 cv::projectPoints (per disegnare l’origine)](https://docs.opencv.org/4.11.0/d9/d0c/group__calib3d.html#ga29ce80c9478b7e0fdb80d594c94c24fa)

---

## 📃 Licenza

Questo progetto è rilasciato con licenza MIT.
