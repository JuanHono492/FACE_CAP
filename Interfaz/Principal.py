import tkinter as tk
import subprocess
import sys

# Obtener el nombre de usuario de los argumentos
username = sys.argv[1] if len(sys.argv) > 1 else None

def cargar_usuarios():
    try:
        root.destroy()  # Cerrar la ventana actual
        subprocess.run(["python", "Interfaz/Data.py"], check=True)
    except subprocess.CalledProcessError as e:
        mostrar_notificacion(f"Error al cargar usuarios: {e}", color="red")

def ver_usuarios_actuales():
    print("Mostrando usuarios actuales...")

def agregar_database():
    try:
        subprocess.run(["python", "Interfaz/Agregarbd.py"], check=True)
    except subprocess.CalledProcessError as e:
        mostrar_notificacion(f"Error al abrir Agregarbd.py: {e}", color="red")

def ejecutar_reconocimiento():
    try:
        subprocess.Popen(["python", "Back/Reconocimiento-gray.py"])
    except Exception as e:
        mostrar_notificacion(f"Error al ejecutar reconocimiento facial: {e}", color="red")

def mostrar_notificacion(mensaje, color="green"):
    notificacion_label.config(text=mensaje, fg=color)
    root.after(2000, limpiar_notificacion)  # Limpiar notificación después de 10 segundos

def limpiar_notificacion():
    notificacion_label.config(text="")

def cerrar_sesion():
    root.destroy()  # Cierra la ventana actual
    subprocess.Popen(["python", "FACE_CAP.py"])  # Vuelve a la pantalla de inicio de sesión

# Crear la ventana principal
root = tk.Tk()
root.title("Tablero principal")

# Configurar el tamaño de la ventana
root.geometry("800x600")
root.configure(bg="#e0f7fa")  # Fondo azul claro

# Crear un frame principal con fondo blanco y borde
main_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
main_frame.pack(expand=True, padx=20, pady=20, fill=tk.BOTH)

# Crear una etiqueta de bienvenida
if username:
    bienvenida_label = tk.Label(main_frame, text=f"Bienvenido, {username}", font=("Arial", 18), bg="white", fg="black")
else:
    bienvenida_label = tk.Label(main_frame, text="Bienvenido", font=("Arial", 18), bg="white", fg="black")
bienvenida_label.pack(pady=10)  # Colocar la etiqueta de bienvenida en el layout

# Crear un frame para la entrada del usuario
input_frame = tk.Frame(main_frame, bg="white")
input_frame.pack(pady=20)

# Etiqueta para notificaciones
notificacion_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#e0f7fa", fg="red")
notificacion_label.pack(pady=10)

# Estilo para los botones
button_style = {"font": ("Arial", 14), "bg": "#004d40", "fg": "white", "activebackground": "#00332d", "activeforeground": "white", "bd": 2, "relief": tk.RAISED, "borderwidth": 3}

# Botón para cargar usuarios
cargar_button = tk.Button(main_frame, text="Cargar Usuarios", command=cargar_usuarios, **button_style)
cargar_button.pack(pady=10, padx=20, fill=tk.BOTH)

# Botón para ver usuarios actuales
ver_button = tk.Button(main_frame, text="Ver Usuarios Actuales", command=ver_usuarios_actuales, **button_style)
ver_button.pack(pady=10, padx=20, fill=tk.BOTH)

# Botón para agregar usuario
agregar_button = tk.Button(main_frame, text="Conectar base de datos", command=agregar_database, **button_style)
agregar_button.pack(pady=10, padx=20, fill=tk.BOTH)

# Botón para ejecutar reconocimiento facial
reconocimiento_button = tk.Button(main_frame, text="Ejecutar Reconocimiento Facial", command=ejecutar_reconocimiento, **button_style)
reconocimiento_button.pack(pady=10, padx=20, fill=tk.BOTH)

# Botón para cerrar sesión
cerrar_sesion_button = tk.Button(main_frame, text="Cerrar Sesión", command=cerrar_sesion, **button_style)
cerrar_sesion_button.pack(pady=10, padx=20, fill=tk.BOTH)

# Iniciar el bucle de la ventana
root.mainloop()
