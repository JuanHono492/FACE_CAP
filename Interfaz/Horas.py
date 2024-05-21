import tkinter as tk
import tkinter.messagebox as tkMessageBox
import json

# Ruta del archivo para guardar la configuración
CONFIG_FILE = "config.json"

# Función para cargar la configuración desde un archivo JSON
def cargar_configuracion():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"desde": "", "hasta": ""}

# Función para guardar la configuración en un archivo JSON
def guardar_configuracion(configuracion):
    with open(CONFIG_FILE, "w") as file:
        json.dump(configuracion, file)

# Crear la ventana principal
root = tk.Tk()
root.title("Configuración de Automatización")

# Crear un frame principal
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack()

# Etiquetas y cuadros de texto para ingresar los horarios de inicio y fin de ejecución
tk.Label(main_frame, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
entrada_desde = tk.Entry(main_frame, width=8)
entrada_desde.grid(row=0, column=1, padx=5, pady=5)

tk.Label(main_frame, text="Hasta:").grid(row=1, column=0, padx=5, pady=5)
entrada_hasta = tk.Entry(main_frame, width=8)
entrada_hasta.grid(row=1, column=1, padx=5, pady=5)

# Botón para guardar la configuración
def guardar_horario():
    desde = entrada_desde.get()
    hasta = entrada_hasta.get()
    configuracion = {"desde": desde, "hasta": hasta}
    guardar_configuracion(configuracion)
    tk.messagebox.showinfo("Horario Guardado", "El horario se ha guardado correctamente.")

boton_guardar = tk.Button(main_frame, text="Guardar Horario", command=guardar_horario)
boton_guardar.grid(row=2, column=0, columnspan=2, pady=10)

# Iniciar el bucle de la ventana
root.mainloop()
