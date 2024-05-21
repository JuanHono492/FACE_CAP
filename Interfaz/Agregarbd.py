import tkinter as tk
import sqlite3
import json
import os

class DatabaseInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Interfaz de Base de Datos")
        self.master.geometry("800x600")
        self.master.configure(bg="#e0f7fa")

        # Variables para almacenar las credenciales de conexión
        self.host_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Cargar datos guardados
        self.load_credentials()

        # Crear elementos de la interfaz
        self.label = tk.Label(master, text="Interfaz de Base de Datos", font=("Arial", 16), bg="#e0f7fa")
        self.label.pack(pady=10)

        # Campos de entrada para las credenciales de conexión
        input_frame = tk.Frame(master, bg="#e0f7fa")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Host:", font=("Arial", 12), bg="#e0f7fa").grid(row=0, column=0, padx=5, pady=5)
        self.host_entry = tk.Entry(input_frame, textvariable=self.host_var, font=("Arial", 12))
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Usuario:", font=("Arial", 12), bg="#e0f7fa").grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(input_frame, textvariable=self.username_var, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Contraseña:", font=("Arial", 12), bg="#e0f7fa").grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(input_frame, textvariable=self.password_var, show="*", font=("Arial", 12))
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        button_frame = tk.Frame(master, bg="#e0f7fa")
        button_frame.pack(pady=20)

        self.connect_button = tk.Button(button_frame, text="Conectar a la base de datos", command=self.connect_to_database, font=("Arial", 12), bg="#004d40", fg="white", activebackground="#00332d", activeforeground="white")
        self.connect_button.grid(row=0, column=0, padx=10, pady=10)

        self.check_connection_button = tk.Button(button_frame, text="Comprobar conexión", command=self.check_connection, font=("Arial", 12), bg="#004d40", fg="white", activebackground="#00332d", activeforeground="white", state=tk.DISABLED)
        self.check_connection_button.grid(row=0, column=1, padx=10, pady=10)

        self.return_button = tk.Button(button_frame, text="Regresar", command=self.return_to_main_menu, font=("Arial", 12), bg="#004d40", fg="white", activebackground="#00332d", activeforeground="white")
        self.return_button.grid(row=0, column=2, padx=10, pady=10)

        self.clear_button = tk.Button(button_frame, text="Desconectar de la base de datos", command=self.clear_credentials, font=("Arial", 12), bg="#c62828", fg="white", activebackground="#8e0000", activeforeground="white")
        self.clear_button.grid(row=0, column=3, padx=10, pady=10)

        self.notification_label = tk.Label(master, text="", font=("Arial", 12), bg="#e0f7fa", fg="red")
        self.notification_label.pack(pady=10)

        # Cerrar la conexión con la base de datos al cerrar la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect_to_database(self):
        try:
            # Aquí puedes utilizar las credenciales ingresadas para conectarte a la base de datos
            host = self.host_var.get()
            username = self.username_var.get()
            password = self.password_var.get()

            # Por ejemplo, puedes usar sqlite3.connect para conectarte a una base de datos SQLite
            # O puedes usar otro método según el tipo de base de datos que estés utilizando
            self.connection = sqlite3.connect(":memory:")  # Conexión temporal para verificar
            self.connection.close()  # Cerrar la conexión temporal
            self.connect_button.config(state=tk.DISABLED)
            self.check_connection_button.config(state=tk.NORMAL)
            self.show_notification("Conexión exitosa a la base de datos.", "green")

            # Guardar credenciales
            self.save_credentials()
        except Exception as e:
            self.show_notification(f"Error al conectar a la base de datos: {e}", "red")

    def check_connection(self):
        try:
            # Aquí puedes realizar una operación para verificar la conexión, por ejemplo, una consulta simple
            self.connection = sqlite3.connect(":memory:")  # Conexión temporal para verificar
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT 1")
            self.connection.close()
            self.show_notification("Conexión establecida.", "green")
        except Exception as e:
            self.show_notification(f"No se pudo establecer la conexión: {e}", "red")

    def return_to_main_menu(self):
        self.close_connection()

    def close_connection(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
        if self.master.winfo_exists():
            self.master.destroy()

    def clear_credentials(self):
        self.host_var.set("")
        self.username_var.set("")
        self.password_var.set("")
        self.connect_button.config(state=tk.NORMAL)
        self.check_connection_button.config(state=tk.DISABLED)
        if os.path.exists("credentials.json"):
            os.remove("credentials.json")
        self.show_notification("Credenciales limpiadas y desconectadas de la base de datos.", "green")

    def on_closing(self):
        self.save_credentials()
        self.close_connection()

    def show_notification(self, message, color):
        self.notification_label.config(text=message, fg=color)
        self.master.after(5000, self.clear_notification)

    def clear_notification(self):
        self.notification_label.config(text="")

    def save_credentials(self):
        credentials = {
            "host": self.host_var.get(),
            "username": self.username_var.get(),
            "password": self.password_var.get()
        }
        with open("credentials.json", "w") as f:
            json.dump(credentials, f)

    def load_credentials(self):
        if os.path.exists("credentials.json"):
            with open("credentials.json", "r") as f:
                credentials = json.load(f)
                self.host_var.set(credentials.get("host", ""))
                self.username_var.set(credentials.get("username", ""))
                self.password_var.set(credentials.get("password", ""))

def main():
    root = tk.Tk()
    app = DatabaseInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
