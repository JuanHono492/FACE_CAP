import cv2
import os
import json

# Cargar el diccionario de nombres desde el archivo JSON
label_to_name_path = os.path.join('2.- Practica', 'label_to_name.json')
with open(label_to_name_path, 'r') as f:
    label_to_name = json.load(f)

# Crear el objeto de reconocimiento facial
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Obtener la ruta completa al archivo 'modelo_entrenado.xml'
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'modelo_entrenado.xml')

# Cargar el modelo entrenado
face_recognizer.read(model_path)

# Inicializar la captura de video
cap = cv2.VideoCapture(0)  # Cambiado para captura desde la cámara
#'2.- Practica/Juan2.mp4'

# Reducir la resolución de captura para mejorar la fluidez
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    # Leer un fotograma del video
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Iterar sobre los rostros detectados
    for (x, y, w, h) in faces:
        # Dibujar un rectángulo alrededor del rostro detectado
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Recortar el rostro detectado para la predicción
        face_roi = gray[y:y + h, x:x + w]

        # Realizar la predicción en el rostro recortado
        label, confidence = face_recognizer.predict(face_roi)

        # Obtener el nombre de la persona reconocida
        if confidence > 99:
            person_name = 'Desconocido'
        else:
            person_name = label_to_name.get(str(label), f'Persona {label}')  # Obtener el nombre del diccionario o asignar uno genérico

        # Escribir el nombre de la persona sobre el cuadro delimitador
        cv2.putText(frame, f'Persona: {person_name}', (x, y - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                    
        cv2.putText(frame, f'Confianza: {confidence}', (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    # Mostrar el fotograma
    cv2.imshow('Reconocimiento facial en video', frame)

    # Salir si se presiona 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
