import tkinter as tk
import subprocess
from Interfaz.addArea import gestionar_areas
from Interfaz.Agregarbd import AgregarBaseDeDatos  # Importar la clase AgregarBaseDeDatos

def principal_view(root, username):
    def cargar_usuarios():
        try:
            for widget in root.winfo_children():
                widget.destroy()
            subprocess.run(["python", "Interfaz/Data.py"], check=True)
        except subprocess.CalledProcessError as e:
            mostrar_notificacion(f"Error al cargar usuarios: {e}", color="red")

    def ver_usuarios_actuales():
        print("Mostrando usuarios actuales...")

    def agregar_database():
        # Abrir la vista de Agregar Base de Datos
        AgregarBaseDeDatos(tk.Toplevel(root))

    def agregar_area():
        gestionar_areas(root, username, principal_view)

    def asignacion_camaras():
        try:
            subprocess.run(["python", "Interfaz/asignar_camaras.py"], check=True)
        except subprocess.CalledProcessError as e:
            mostrar_notificacion(f"Error al abrir Asignar_camaras.py: {e}", color="red")

    def ejecutar_reconocimiento():
        try:
            subprocess.Popen(["python", "Back/Reconocimiento-gray.py"])
        except Exception as e:
            mostrar_notificacion(f"Error al ejecutar reconocimiento facial: {e}", color="red")

    def mostrar_notificacion(mensaje, color="green"):
        notificacion_label.config(text=mensaje, fg=color)
        root.after(2000, limpiar_notificacion)

    def limpiar_notificacion():
        notificacion_label.config(text="")

    def cerrar_sesion():
        for widget in root.winfo_children():
            widget.destroy()
        cargar_login_view(root)

    root.geometry("800x650")
    root.configure(bg="#e0f7fa")

    main_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
    main_frame.pack(expand=True, padx=20, pady=20, fill=tk.BOTH)

    bienvenida_label = tk.Label(main_frame, text=f"Bienvenido, {username}", font=("Arial", 18), bg="white", fg="black")
    bienvenida_label.pack(pady=10)

    notificacion_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#e0f7fa", fg="red")
    notificacion_label.pack(pady=10)

    button_style = {"font": ("Arial", 14), "bg": "#004d40", "fg": "white", "activebackground": "#00332d", "activeforeground": "white", "bd": 2, "relief": tk.RAISED, "borderwidth": 3}

    tk.Button(main_frame, text="Agregar áreas", command=agregar_area, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Asignar cámaras", command=asignacion_camaras, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Cargar Usuarios", command=cargar_usuarios, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Ver Usuarios Actuales", command=ver_usuarios_actuales, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Conectar base de datos", command=agregar_database, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Ejecutar Reconocimiento Facial", command=ejecutar_reconocimiento, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)
    tk.Button(main_frame, text="Cerrar Sesión", command=cerrar_sesion, **button_style).pack(pady=10, padx=20, fill=tk.BOTH)

def cargar_login_view(root):
    for widget in root.winfo_children():
        widget.destroy()
    # Aquí debes cargar el contenido del archivo original FACE_CAP.py que maneja la vista de inicio de sesión

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Reconocimiento Facial")
    root.geometry("820x650")
    root.configure(bg="#00AA66")

    main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid")
    main_frame.pack(expand=True, padx=20, pady=20)

    logo_image = tk.PhotoImage(file="Interfaz/logo.png")
    logo_label = tk.Label(main_frame, image=logo_image, bg="#ffffff")
    logo_label.grid(row=0, column=0, columnspan=2, pady=20)

    form_frame = tk.Frame(main_frame, bg="#ffffff")
    form_frame.grid(row=1, column=0, columnspan=2, pady=20)

    tk.Label(form_frame, text="Nombre de usuario:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(form_frame, font=("Arial", 12))
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Contraseña:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    password_entry = tk.Entry(form_frame, show="*", font=("Arial", 12))
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    toggle_button = tk.Button(form_frame, text="Mostrar contraseña", font=("Arial", 12), bg="#004d40", fg="#ffffff", activebackground="#00332d", activeforeground="#ffffff", bd=2, relief=tk.RAISED, borderwidth=3)
    toggle_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    login_button = tk.Button(form_frame, text="Iniciar sesión", font=("Arial", 12), bg="#004d40", fg="#ffffff", activebackground="#00332d", activeforeground="#ffffff", bd=2, relief=tk.RAISED, borderwidth=3)
    login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    register_button = tk.Button(form_frame, text="Registrar", font=("Arial", 12), bg="#004d40", fg="#ffffff", activebackground="#00332d", activeforeground="#ffffff", bd=2, relief=tk.RAISED, borderwidth=3)
    register_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    loading_label = tk.Label(form_frame, text="Cargando...", font=("Arial", 12), bg="#ffffff")

    root.mainloop()
