import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Verificar las credenciales (aquí puedes implementar tu lógica de autenticación)
    if username == "usuario" and password == "contraseña":
        # Mostrar animación de carga durante 2 segundos
        loading_label.grid(row=4, column=0, columnspan=2, pady=10)
        root.after(2000, lambda: open_data_section(username))  # Pasar el nombre de usuario
    else:
        messagebox.showerror("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos")

def open_data_section(username):
    loading_label.grid_forget()  # Ocultar la animación de carga
    root.destroy()  # Cerrar la ventana Login
    # Abre el archivo Principal.py y pasa el nombre de usuario como argumento
    subprocess.Popen(["python", "Interfaz/Principal.py", username])

def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
    else:
        password_entry.config(show="")

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")

# Configurar el tamaño de la ventana
root.geometry("800x600")  # Puedes ajustar el tamaño según sea necesario

# Estilos
root.configure(bg="#00AA66")  # Fondo verde más claro

# Crear un frame principal para centrar el contenido con fondo blanco y borde
main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid")
main_frame.pack(expand=True, padx=20, pady=20)

# Cargar la imagen con Pillow
logo_image = Image.open("Interfaz/logo.png")
logo = ImageTk.PhotoImage(logo_image)
# Reemplaza "logo.png" con la ruta de tu archivo de imagen
logo_label = tk.Label(main_frame, image=logo, bg="#ffffff")
logo_label.grid(row=0, column=0, columnspan=2, pady=20)

# Crear un frame para el formulario
form_frame = tk.Frame(main_frame, bg="#ffffff")
form_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Crear etiquetas y campos de entrada para el inicio de sesión
username_label = tk.Label(form_frame, text="Nombre de usuario:", font=("Arial", 12), bg="#ffffff")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(form_frame, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = tk.Label(form_frame, text="Contraseña:", font=("Arial", 12), bg="#ffffff")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(form_frame, show="*", font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=10, pady=5)

toggle_button = tk.Button(form_frame, text="Mostrar contraseña", command=toggle_password_visibility, font=("Arial", 12), bg="#004d40", fg="#ffffff", activebackground="#00332d", activeforeground="#ffffff", bd=2, relief=tk.RAISED, borderwidth=3)
toggle_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

login_button = tk.Button(form_frame, text="Iniciar sesión", command=login, font=("Arial", 12), bg="#004d40", fg="#ffffff", activebackground="#00332d", activeforeground="#ffffff", bd=2, relief=tk.RAISED, borderwidth=3)
login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Etiqueta para la animación de carga
loading_label = tk.Label(form_frame, text="Cargando...", font=("Arial", 12), bg="#ffffff")

# Iniciar el bucle de la ventana
root.mainloop()
