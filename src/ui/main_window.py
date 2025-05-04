# src/ui/main_window.py
import customtkinter as ctk
# Importar TODOS los frames principales que gestionará
from .frames.main_menu_frame import MainMenuFrame
from .frames.days_calculator_frame import DaysCalculatorFrame
from .frames.cesantias_frame import CesantiasFrame

class MainWindow(ctk.CTk):
    """
    Ventana principal de la aplicación. Gestiona y muestra los diferentes frames (vistas).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Calculadora de Liquidación Laboral (COL)")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 950 # Ajustar tamaño
        height = 600 # Ajustar tamaño
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.minsize(700, 500)

        # --- Contenedor Principal ---
        # Un frame que ocupa toda la ventana para poner los otros frames encima
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # --- Diccionario para almacenar los frames ---
        self.frames = {}

        # --- Crear e inicializar todos los frames ---
        # Usamos lambda para pasar 'container' como master a cada frame
        for F in (MainMenuFrame, DaysCalculatorFrame, CesantiasFrame):
            page_name = F.__name__
            frame = F(master=container)
            self.frames[page_name] = frame
            # Colocar todos en el mismo lugar, el que esté arriba es visible
            frame.grid(row=0, column=0, sticky="nsew")

        # --- Mostrar el frame inicial ---
        self.show_frame("MainMenuFrame")

    def show_frame(self, page_name: str):
        """Muestra el frame especificado por page_name."""
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise() # Trae el frame al frente
        else:
            print(f"Advertencia: No se encontró el frame '{page_name}'")

    # --- Métodos para obtener instancias de frames específicos (para el controlador) ---
    def get_frame(self, page_name: str):
        """Obtiene la instancia de un frame por su nombre de clase."""
        return self.frames.get(page_name)