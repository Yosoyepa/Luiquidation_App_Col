# main.py
import customtkinter as ctk
from src.ui.main_window import MainWindow
from src.controllers.main_controller import MainController
# Importar configuraciones si se usan para la UI, ej: from config import settings_loader

# --- Configuración Inicial de Apariencia (Ejemplo) ---
# Idealmente, cargar desde config/parameters.json si existe
ctk.set_appearance_mode("System")  # O "Light", "Dark"
ctk.set_default_color_theme("blue") # O "green", "dark-blue"

def main():
    """Función principal para iniciar la aplicación."""
    app = MainWindow()
    controller = MainController(view=app) # Inyectar la vista al controlador
    app.mainloop()

if __name__ == "__main__":
    main()