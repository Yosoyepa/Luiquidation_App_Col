# src/ui/frames/days_calculator_frame.py
import customtkinter as ctk
from .input_frame import InputFrame # Importa el frame de inputs existente
from .results_frame import ResultsFrame # Importa el frame de resultados existente

class DaysCalculatorFrame(ctk.CTkFrame):
    """
    Frame que encapsula la funcionalidad de cálculo de días 30/360.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Input frame toma espacio
        self.grid_rowconfigure(1, weight=0) # Results frame fijo
        self.grid_rowconfigure(2, weight=0) # Botón back fijo

        # Instanciar los frames originales dentro de este
        self.input_frame = InputFrame(self, fg_color="transparent")
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.results_frame = ResultsFrame(self, height=50)
        self.results_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.back_button = ctk.CTkButton(self, text="Volver al Menú", fg_color="gray")
        self.back_button.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")

    # Métodos para exponer funcionalidad interna al controlador
    def get_input_frame(self) -> InputFrame:
        return self.input_frame

    def get_results_frame(self) -> ResultsFrame:
        return self.results_frame

    def set_back_command(self, command):
        """Asigna comando al botón Volver."""
        self.back_button.configure(command=command)