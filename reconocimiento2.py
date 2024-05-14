import cv2
import mediapipe as mp

# Inicializar el módulo de MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Iniciar la captura de vídeo desde la cámara
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    if not ret:
        break

    # Convertir la imagen a RGB (MediaPipe utiliza imágenes en formato RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar la pose en el frame
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Dibujar los puntos clave y conexiones en el frame
        mp_drawing = mp.solutions.drawing_utils
        annotated_frame = frame.copy()  # Hacer una copia para no modificar el frame original
        mp_drawing.draw_landmarks(annotated_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Mostrar el frame con la pose estimada
        cv2.imshow('Estimación de Postura', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
