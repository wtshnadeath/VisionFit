import cv2
import os

# Ruta al archivo XML que contiene el modelo de detección de cuerpo completo
xml_path = "C:/Users/nadia/OneDrive/Documents/OCTAVOSEMESTRE/TMPI/Practicas/Proyecto/haarcascade_fullbody.xml"

# Inicializar el clasificador Haar
clasificador_cuerpo = cv2.CascadeClassifier(xml_path)

# Iniciar la captura de vídeo desde la cámara
video = cv2.VideoCapture(0)

while True:
    # Leer un cuadro del vídeo
    ret, frame = video.read()

    if not ret:
        break

    # Convertir el cuadro a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar cuerpos en el cuadro
    cuerpos = clasificador_cuerpo.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dibujar rectángulos alrededor de los cuerpos detectados
    for (x, y, w, h) in cuerpos:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostrar el cuadro con los rectángulos dibujados
    cv2.imshow('Detección de Cuerpos', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar las ventanas
video.release()
cv2.destroyAllWindows()
