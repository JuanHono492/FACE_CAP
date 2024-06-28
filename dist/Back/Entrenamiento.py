import cv2
import os
import numpy as np
import shutil
import json

# Directorio donde se encuentran los datos de entrenamiento
dataPath = 'Data'
peopleList = os.listdir(dataPath)
print('Lista de personas:', peopleList)

labels = []
facesData = []
label_to_name_path = os.path.join('Back', 'label_to_name.json')

# Cargar o crear el diccionario de nombres y áreas
if os.path.exists(label_to_name_path):
    with open(label_to_name_path, 'r') as f:
        label_to_name = json.load(f)
else:
    label_to_name = {}

# Obtener la última etiqueta asignada si el diccionario no está vacío
last_label = int(max(label_to_name.keys(), default=0))

# Definir el tamaño deseado para las imágenes de entrenamiento
desired_size = (100, 100)

# Lista para mantener el orden de las etiquetas
label_order = []

for nameDir in peopleList:
    personPath = os.path.join(dataPath, nameDir)
    print('Leyendo las imágenes de', nameDir)

    # Incrementar el valor de la etiqueta para cada nueva persona
    last_label += 1

    # Aquí deberías cargar las áreas correspondientes al usuario desde un archivo o una variable global
    # Por ahora, usaremos un ejemplo fijo
    areas = ["Area de TI", "Area de soporte"]

    # Agregar el nombre de la persona y las áreas al diccionario si no existen
    if str(last_label) not in label_to_name:
        label_to_name[str(last_label)] = {
            "nombre": nameDir,
            "areas": areas
        }
        label_order.append(str(last_label))

    for fileName in os.listdir(personPath):
        print('Rostro:', nameDir + '/' + fileName)
        labels.append(last_label)
        # Leer la imagen y redimensionarla al tamaño deseado
        imagePath = os.path.join(personPath, fileName)
        image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        if image is not None:
            resized_image = cv2.resize(image, desired_size)
            facesData.append(resized_image)
        else:
            print(f"No se pudo leer la imagen: {imagePath}")

# Convertir las listas de etiquetas y datos de rostros en matrices numpy
labels = np.array(labels)
facesData = np.array(facesData)

# Crear el objeto de reconocimiento facial o cargar el modelo existente
model_path = os.path.join('Back', 'modelo_entrenado.xml')
if os.path.exists(model_path):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(model_path)
    print("Modelo existente cargado desde:", model_path)
else:
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("Creando un nuevo modelo...")

# Entrenar el modelo con el nuevo conjunto de datos
print("Añadiendo nuevo entrenamiento al modelo...")
face_recognizer.update(facesData, labels)
face_recognizer.save(model_path)
print("Modelo actualizado y guardado en:", model_path)

# Guardar el diccionario de nombres y áreas en el archivo JSON respetando el orden de etiquetas
with open(label_to_name_path, 'w') as f:
    ordered_label_to_name = {key: label_to_name[key] for key in sorted(label_to_name, key=int)}
    json.dump(ordered_label_to_name, f, indent=4)

# Borrar las imágenes de entrenamiento después de que el modelo ha sido creado
print("Borrando imágenes de entrenamiento...")
shutil.rmtree(dataPath)
print("Imágenes de entrenamiento borradas.")
