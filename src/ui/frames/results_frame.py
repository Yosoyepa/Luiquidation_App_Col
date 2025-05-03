# src/ui/frames/results_frame.py
import customtkinter as ctk

class ResultsFrame(ctk.CTkFrame):
    """
    Frame que muestra los resultados de los cálculos.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.result_label_var = ctk.StringVar(value="Días calculados: -")
        self.result_label = ctk.CTkLabel(
            self,
            textvariable=self.result_label_var,
            font=ctk.CTkFont(size=14, weight="bold") # Fuente más grande
        )

        self.result_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def update_result(self, text: str):
        """Actualiza el texto de la etiqueta de resultado."""
        self.result_label_var.set(text)