import cv2
import mediapipe as mp # type: ignore
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Inicializar el módulo de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils  # Importar el módulo de dibujo de MediaPipe

# Capturar video desde la cámara
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Leer un frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el frame a color (RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Procesar la imagen para detectar manos
    results = hands.process(rgb_frame)
    #print(results.multi_hand_landmarks)
    # Dibujar la detección de manos si se detectan manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar los landmarks de la mano
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            """ # Comprobar si el landmark de la punta del dedo índice está presente
            for id, lm in enumerate(hand_landmarks.landmark):
                if id == 8:  # La punta del dedo índice
                    # Si el landmark está presente, mostrar un mensaje en la consola
                    print("¡Punta del dedo índice detectada!") """
            

    # Mostrar el frame
    cv2.imshow('Hand Tracking', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()