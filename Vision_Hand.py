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

            # Calcular la distancia entre el centro de la palma y las puntas de los dedos
            palm_center = hand_landmarks.landmark[0]
            finger_tips = [hand_landmarks.landmark[i] for i in [4, 8, 12, 16, 20]]
            distances = [((palm_center.x - tip.x)**2 + (palm_center.y - tip.y)**2)**0.5 for tip in finger_tips]

            # Si todas las distancias son menores que un cierto umbral, la mano está empuñada
            if all(distance < 0.1 for distance in distances):  # Ajusta el umbral según sea necesario
                print("¡Mano empuñada detectada!")
                
                # Calcular en qué cuadrante está el centro de la mano
                x = int(palm_center.x * width)
                y = int(palm_center.y * height)
                quadrant = (y // y_mid) * 3 + (x // x_mid) + 1
                print(f"La mano está en el cuadrante {quadrant}")
            
            # Calcular el tamaño de la mano en la imagen
            x_values = [lm.x for lm in hand_landmarks.landmark]
            y_values = [lm.y for lm in hand_landmarks.landmark]
            hand_width = max(x_values) - min(x_values)
            hand_height = max(y_values) - min(y_values)
            hand_size = hand_width * hand_height
            print(f"El tamaño de la mano en la imagen es {hand_size}")

            """ # Comprobar si el landmark de la punta del dedo índice está presente
            for id, lm in enumerate(hand_landmarks.landmark):
                if id == 8:  # La punta del dedo índice
                    # Si el landmark está presente, mostrar un mensaje en la consola
                    print("¡Punta del dedo índice detectada!") """
             # Calcular el bounding box de la mano
            
            x_min = min(lm.x for lm in hand_landmarks.landmark)
            y_min = min(lm.y for lm in hand_landmarks.landmark)
            x_max = max(lm.x for lm in hand_landmarks.landmark)
            y_max = max(lm.y for lm in hand_landmarks.landmark)

            # Convertir las coordenadas del bounding box a píxeles
            height, width, _ = frame.shape
            x_min = int(x_min * width)
            y_min = int(y_min * height)
            x_max = int(x_max * width)
            y_max = int(y_max * height)

            # Dibujar el bounding box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Verde, grosor 2


    # Mostrar el frame
    cv2.imshow('Hand Tracking', frame)
    
    # Obtener las dimensiones del frame
    height, width, _ = frame.shape

    # Calcular las coordenadas de las líneas
    x_mid = width // 3
    y_mid = height // 3

    # Dibujar las líneas verticales
    cv2.line(frame, (x_mid, 0), (x_mid, height), (0, 255, 0), 2)  # Verde, grosor 2
    cv2.line(frame, (2 * x_mid, 0), (2 * x_mid, height), (0, 255, 0), 2)  # Verde, grosor 2

    # Dibujar las líneas horizontales
    cv2.line(frame, (0, y_mid), (width, y_mid), (0, 255, 0), 2)  # Verde, grosor 2
    cv2.line(frame, (0, 2 * y_mid), (width, 2 * y_mid), (0, 255, 0), 2)  # Verde, grosor 2

    # Mostrar el frame con la cuadrícula
    cv2.imshow('Hand Tracking', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()