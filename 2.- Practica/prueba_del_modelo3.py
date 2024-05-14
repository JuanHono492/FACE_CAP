import cv2
import os
import json
import numpy as np

# Cargar el modelo entrenado
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
model_path = '2.- Practica/modelo_entrenado.xml'
face_recognizer.read(model_path)

# Cargar el diccionario de nombres
with open('2.- Practica/label_to_name.json', 'r') as f:
    label_to_name = json.load(f)

# Inicializar la captura de video
video_path = '2.- Practica/Juan.mp4'
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    label, confidence = face_recognizer.predict(gray)

    # Obtener el nombre de la persona reconocida
    if label in label_to_name:
        person_name = label_to_name[label]
    else:
        person_name = 'Desconocido'

    # Mostrar el resultado en el fotograma
    cv2.putText(frame, f'Persona detectada: {person_name}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Reconocimiento facial en video', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
