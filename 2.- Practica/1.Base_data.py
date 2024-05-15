import os
import cv2
import imutils

# Solicitar el nombre del usuario
print('Captura de datos para el entrenamiento del modelo de reconocimiento facial')
print('Ingresa tu nombre')
nombre = input('Nombre: ')

# Definir el nombre de la persona y la ruta de los datos
dataPath = '1.- Data'  # Asegúrate de que esta carpeta existe
personPath = os.path.join(dataPath, nombre)

# Crear la carpeta si no existe
if not os.path.exists(personPath):
    print(f'Carpeta creada: {personPath}')
    os.makedirs(personPath)

# Inicializar la captura de video
cap = cv2.VideoCapture('2.- Practica/Kenneth.mp4')
print('Capturando datos de video')

count = 0
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=640)

    # Convertir el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el fotograma
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Redimensionar el rostro capturado al tamaño deseado (50x50)
        resized_face = cv2.resize(gray[y:y+h, x:x+w], (50, 50))

        # Guardar múltiples imágenes del rostro redimensionado
        for i in range(2):
            cv2.imwrite(os.path.join(personPath, f'rostro_{count}.jpg'), resized_face)
            count += 1

        # Mostrar feedback visual
        cv2.putText(frame, f'Capturado: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Mostrar el fotograma con los rostros detectados
    cv2.imshow('frame', frame)

    # Salir del bucle si se presiona 'Esc' o se alcanza el límite de capturas
    if cv2.waitKey(1) == 27 or count >= 200:
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

print(f'Captura completada. Se guardaron {count} imágenes en {personPath}')
