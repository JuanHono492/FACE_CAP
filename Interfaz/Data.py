import os
import cv2
import imutils
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import subprocess
import shutil
from tkinter import ttk

# Lista para almacenar los usuarios capturados
usuarios_capturados = []

# Función para capturar datos desde la cámara
def capturar_camara(nombre):
    dataPath = 'Data'
    personPath = os.path.join(dataPath, nombre)

    if not os.path.exists(personPath):
        os.makedirs(personPath)
        mostrar_notificacion(f'Carpeta creada: {personPath}', color= str("green"))

    cap = cv2.VideoCapture(0)  # Cámara por defecto
    mostrar_notificacion('Capturando datos desde la cámara...', color= str("green"))

    count = 0
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            resized_face = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
            for i in range(2):
                cv2.imwrite(os.path.join(personPath, f'rostro_{count}.jpg'), resized_face)
                count += 1
            cv2.putText(frame, f'Capturado: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Convertir el fotograma de OpenCV a un formato compatible con Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Mostrar la imagen en el widget Label
        label.imgtk = imgtk
        label.configure(image=imgtk)
        root.update()  # Actualizar la interfaz

        if cv2.waitKey(1) == 27 or count >= 200:
            break

    cap.release()
    cv2.destroyAllWindows()
    usuarios_capturados.append({"nombre": nombre, "rostros": count})
    actualizar_tabla()
    mostrar_notificacion(f'Captura completada. Se guardaron {count} imágenes en {personPath}' , color= str("green"))
    limpiar_formulario()


def capturar_desde_archivo(nombre):
    dataPath = 'Data'
    personPath = os.path.join(dataPath, nombre)

    if not os.path.exists(personPath):
        os.makedirs(personPath)
        mostrar_notificacion(f'Carpeta creada: {personPath}', color=str("green"))

    video_path = filedialog.askopenfilename(title="Seleccionar archivo de video", filetypes=[("Archivos de video", "*.mp4 *.avi")])
    if not video_path:
        mostrar_notificacion("No se seleccionó ningún archivo de video.")
        return

    cap = cv2.VideoCapture(video_path)
    mostrar_notificacion('Capturando datos desde el archivo de video...', color=str("green"))

    count = 0
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=200)  # Redimensionar a 200x??? manteniendo la relación de aspecto
        frame = centrar_imagen(frame, 200, 200)  # Centrar el fotograma en 200x200

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            resized_face = cv2.resize(gray[y:y + h, x:x + w], (50, 50))
            for i in range(2):
                cv2.imwrite(os.path.join(personPath, f'rostro_{count}.jpg'), resized_face)
                count += 1
            cv2.putText(frame, f'Capturado: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Convertir el fotograma de OpenCV a un formato compatible con Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Mostrar la imagen en el widget Label
        label.imgtk = imgtk
        label.configure(image=imgtk)
        root.update()  # Actualizar la interfaz

        if cv2.waitKey(1) == 27 or count >= 200:
            break

    cap.release()
    cv2.destroyAllWindows()
    usuarios_capturados.append({"nombre": nombre, "rostros": count})
    actualizar_tabla()
    mostrar_notificacion(f'Captura completada. Se guardaron {count} imágenes en {personPath}', color=str("green"))
    limpiar_formulario()



def centrar_imagen(frame, width, height):
    """
    Función para centrar una imagen en un cuadro de tamaño específico.
    :param frame: La imagen para centrar.
    :param width: Ancho deseado del cuadro.
    :param height: Altura deseada del cuadro.
    :return: La imagen centrada.
    """
    h, w = frame.shape[:2]
    if h < height or w < width:
        # Si la imagen es más pequeña que el cuadro, redimensionarla
        frame = cv2.resize(frame, (width, height))
        return frame
    else:
        top = (h - height) // 2
        bottom = h - top - height
        left = (w - width) // 2
        right = w - left - width
        return cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))



# Función para limpiar el formulario y restaurar la interfaz
def limpiar_formulario():
    nombre_entry.delete(0, tk.END)
    label.configure(image='')  # Limpiar la imagen mostrada

# Función para manejar el botón de captura de datos
def capturar_datos():
    nombre = nombre_entry.get()
    if nombre:
        if opcion_var.get() == 0:  # Si se selecciona la opción de captura desde la cámara
            threading.Thread(target=capturar_camara, args=(nombre,)).start()
        else:  # Si se selecciona la opción de captura desde un archivo de video
            threading.Thread(target=capturar_desde_archivo, args=(nombre,)).start()
    else:
        mostrar_notificacion("El nombre no puede estar vacío.")


# Función para mostrar notificaciones temporales
def mostrar_notificacion(mensaje, color="green"):
    notificacion_label.config(text=mensaje, fg=color)
    root.after(5000, limpiar_notificacion)  # Limpiar notificación después de 5 segundos

# Función para limpiar notificaciones
def limpiar_notificacion():
    notificacion_label.config(text="")

# Función para subir datos al modelo
def subir_datos_al_modelo():
    try:
        subprocess.run(["python", "Back/Entrenamiento.py"], check=True)
        limpiar_tabla()
        mostrar_notificacion('Datos subidos correctamente')
    except subprocess.CalledProcessError as e:
        mostrar_notificacion1(f"Error al subir datos al modelo: {e}")


def volver_actividad_anterior():
    # volver a la actividad anterior
    try:
        root.destroy()
        subprocess.run(["python", "Interfaz/Principal.py"], check=True)
    except Exception as e:
        print("Error al volver:", e)


# Función para mostrar notificaciones temporales
def mostrar_notificacion1(mensaje, color="red"):
    notificacion_label.config(text=mensaje, fg=color)
    root.after(10000, limpiar_notificacion)  # Limpiar notificación después de 10 segundos


# Crear la ventana principal
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", lambda: None) # Deshabilitar el cierre de la ventana
root.title("Captura de Datos para Entrenamiento Facial")
root.geometry("800x700")
root.resizable(False, False)
root.configure(bg="#e0f7fa")

# Estilos
estilo_label = {"font": ("Arial", 14), "bg": "#e0f7fa"}
estilo_entry = {"font": ("Arial", 14), "bd": 2, "relief": "solid"}
estilo_button = {"font": ("Arial", 14), "bg": "#004d40", "fg": "white", "activebackground": "#00332d", "activeforeground": "white", "bd": 2, "relief": tk.RAISED, "borderwidth": 3}

# Crear un frame principal con fondo blanco y borde
main_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
main_frame.pack(expand=True, padx=20, pady=20, fill=tk.BOTH)

# Crear etiquetas y campos de entrada en el frame principal
nombre_label = tk.Label(main_frame, text="Nombre completo:", **estilo_label)
nombre_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
nombre_entry = tk.Entry(main_frame, **estilo_entry)
nombre_entry.grid(row=0, column=1, padx=10, pady=5)

# Opciones para capturar datos desde la cámara o desde un archivo de video
opcion_var = tk.IntVar()
camara_radio = tk.Radiobutton(main_frame, text="Usar cámara", variable=opcion_var, value=0, **estilo_label)
camara_radio.grid(row=1, column=0, padx=10, pady=5, sticky="w")
archivo_radio = tk.Radiobutton(main_frame, text="Usar archivo de video", variable=opcion_var, value=1, **estilo_label)
archivo_radio.grid(row=1, column=1, padx=10, pady=5, sticky="w")
# Establecer el tamaño fijo de los radio botones
camara_radio.config(width=20, height=4)
archivo_radio.config(width=20, height=4)

# Widget Label para mostrar la captura de la cámara
label = tk.Label(main_frame, bg="#ffffff")
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Botón para capturar datos
capturar_button = tk.Button(main_frame, text="Capturar Datos", command=capturar_datos, **estilo_button)
capturar_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Botón para subir datos al modelo
subir_button = tk.Button(main_frame, text="Subir Datos al Modelo", command=subir_datos_al_modelo, **estilo_button)
subir_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Botón para volver a la actividad anterior
volver_button = tk.Button(main_frame, text="Volver", command=volver_actividad_anterior, **estilo_button)
volver_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Label para notificaciones
notificacion_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#e0f7fa", fg="red")
notificacion_label.grid(row=6, column=0, columnspan=2, padx=10)

# Centrar los widgets dentro del frame principal
for child in main_frame.winfo_children():
    child.grid_configure(padx=10, pady=5)

# Tabla para mostrar usuarios agregados
tabla_frame = tk.Frame(main_frame, bg="white", bd=2, relief="solid")
tabla_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Configurar la tabla
tabla = ttk.Treeview(tabla_frame, columns=("Nombre", "Rostros Capturados", "Borrar"), show="headings")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Rostros Capturados", text="Rostros Capturados")
tabla.heading("Borrar", text="Borrar")
tabla.pack(fill="both", expand=True)  # Empaqueta la tabla dentro del frame


# Función para actualizar la tabla con los usuarios capturados
def actualizar_tabla():
    # Limpiar la tabla
    for i in tabla.get_children():
        tabla.delete(i)
    # Agregar usuarios capturados a la tabla
    for usuario in usuarios_capturados:
        tabla.insert("", "end", values=(usuario["nombre"], usuario["rostros"]))

def limpiar_tabla():
    for i in tabla.get_children():
        tabla.delete(i)


# Cargar la imagen de eliminar
imagen_eliminar = tk.PhotoImage(file="Interfaz/eliminar.png")

def borrar_usuario():
    selected_item = tabla.selection()
    if selected_item:
        # Obtener el nombre del usuario seleccionado
        usuario_seleccionado = tabla.item(selected_item)['values'][0]
        
        # Eliminar la carpeta del usuario seleccionado
        data_path = '1.- Data'
        person_path = os.path.join(data_path, usuario_seleccionado)
        if os.path.exists(person_path):
            shutil.rmtree(person_path)
        
        # Eliminar el usuario de la lista de usuarios capturados
        for usuario in usuarios_capturados:
            if usuario['nombre'] == usuario_seleccionado:
                usuarios_capturados.remove(usuario)
                break
        
        # Eliminar la fila seleccionada de la tabla
        tabla.delete(selected_item)


# Iniciar el bucle de la ventana
root.mainloop()