# src/ui/main_window.py
import customtkinter as ctk
from .frames.input_frame import InputFrame
from .frames.results_frame import ResultsFrame

class MainWindow(ctk.CTk):
    """
    Ventana principal de la aplicación de Liquidaciones.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Calculadora de Liquidación Laboral (COL)")
        # Obtener dimensiones pantalla para centrar (opcional)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 900 # Ancho deseado
        height = 300 # Alto deseado (ajustar según contenido)
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}') # Tamaño y posición inicial
        self.minsize(600, 250) # Tamaño mínimo

        # Configurar grid layout principal (1 columna, 2 filas)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Fila de inputs toma espacio extra
        self.grid_rowconfigure(1, weight=0) # Fila de resultados tamaño fijo

        # --- Crear Frames ---
        self.input_frame = InputFrame(self, fg_color="transparent")
        self.input_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        self.results_frame = ResultsFrame(self, height=50) # Altura fija para resultados
        self.results_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

    # Métodos para que el controlador acceda a los frames si es necesario
    def get_input_frame(self) -> InputFrame:
        return self.input_frame

    def get_results_frame(self) -> ResultsFrame:
        return self.results_frame