import cv2
import os

# Crear el objeto de reconocimiento facial
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Obtener la ruta completa al archivo 'modelo_entrenado.xml'
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir,'modelo_entrenado.xml')

# Cargar el modelo entrenado
face_recognizer.read(model_path)

# Cargar la imagen a comparar
image_path = 'Images/Juan3.jpg'

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Realizar la predicción
label, confidence = face_recognizer.predict(image)

# Obtener el nombre de la persona reconocida
# (asumiendo que la etiqueta corresponde a la posición en la lista peopleList)
peopleList = ['Persona 1', 'Persona 2', 'Persona 3', '...']
person_name = peopleList[label]

# Mostrar el resultado
print(f'La imagen pertenece a: {person_name} con una confianza de {confidence}')