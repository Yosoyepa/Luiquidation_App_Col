# src/ui/main_window.py
import customtkinter as ctk
from tkinter import Frame  # Regular tkinter Frame as a fallback
# Importar TODOS los frames principales que gestionará
from .frames.main_menu_frame import MainMenuFrame
from .frames.days_calculator_frame import DaysCalculatorFrame
from .frames.cesantias_frame import CesantiasFrame
from .frames.intereses_cesantias_frame import InteresesCesantiasFrame
from .frames.prima_frame import PrimaFrame

class MainWindow(ctk.CTk):
    """
    Ventana principal de la aplicación. Gestiona y muestra los diferentes frames (vistas).
    """
    def __init__(self, *args, **kwargs):
        # Disable scaling completely
        ctk.deactivate_automatic_dpi_awareness()
        
        # Initialize with no scaling parameters in kwargs
        if 'fg_color' in kwargs:
            del kwargs['fg_color']
        if 'width' in kwargs:
            del kwargs['width']
        if 'height' in kwargs:
            del kwargs['height']
            
        super().__init__(*args, **kwargs)

        self.title("Calculadora de Liquidación Laboral (COL)")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 950
        height = 600
        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2))
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.minsize(700, 500)

        # --- Contenedor Principal ---
        # Use standard tkinter Frame instead of CTkFrame to avoid scaling issues
        container = Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # --- Diccionario para almacenar los frames ---
        self.frames = {}

        # --- Crear e inicializar todos los frames ---
        for F in (MainMenuFrame, DaysCalculatorFrame, CesantiasFrame, InteresesCesantiasFrame, PrimaFrame):
            page_name = F.__name__
            # Crear instancia pasando el contenedor como master
            frame = F(master=container)
            self.frames[page_name] = frame
            # Colocar todos en el mismo lugar
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

    def get_frame(self, page_name: str):
        """Obtiene la instancia de un frame por su nombre de clase."""
        return self.frames.get(page_name)