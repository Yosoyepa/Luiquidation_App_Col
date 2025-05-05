# src/ui/frames/prima_frame.py
import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
import src.ui.theme as theme
from typing import Dict, Any

class PrimaFrame(ctk.CTkFrame):
    """
    Frame para la interfaz de cálculo de Prima de Servicios.
    """
    def __init__(self, master, **kwargs):
        kwargs.update({"fg_color": theme.COLOR_MAIN_BG})
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # --- Widgets ---
        self.label_salario = ctk.CTkLabel(self, text="Salario Básico Mensual (Sin Aux. Transporte):")
        self.entry_salario = ctk.CTkEntry(self, placeholder_text="Ej: 1300000")

        self.label_inicio = ctk.CTkLabel(self, text="Fecha Inicio Periodo:")
        self.date_entry_inicio = DateEntry(self, date_pattern='yyyy-mm-dd', locale='es_CO')
        self.date_entry_inicio.config({"borderwidth": 1})

        self.label_fin = ctk.CTkLabel(self, text="Fecha Fin Periodo:")
        self.date_entry_fin = DateEntry(self, date_pattern='yyyy-mm-dd', locale='es_CO')
        self.date_entry_fin.config({"borderwidth": 1})

        self.calculate_button = ctk.CTkButton(self, text="Calcular Prima")

        # Etiquetas para resultados
        self.result_s1_label_var = ctk.StringVar(value="Prima Semestre 1: -")
        self.result_s1_label = ctk.CTkLabel(self, textvariable=self.result_s1_label_var, font=ctk.CTkFont(family=theme.FONT_FAMILY_DEFAULT, size=13))

        self.result_s2_label_var = ctk.StringVar(value="Prima Semestre 2: -")
        self.result_s2_label = ctk.CTkLabel(self, textvariable=self.result_s2_label_var, font=ctk.CTkFont(family=theme.FONT_FAMILY_DEFAULT, size=13))

        self.result_total_label_var = ctk.StringVar(value="Prima Total Periodo: -")
        self.result_total_label = ctk.CTkLabel(self, textvariable=self.result_total_label_var, font=ctk.CTkFont(family=theme.FONT_FAMILY_DEFAULT, size=13, weight="bold"))

        self.back_button = ctk.CTkButton(self, text="Volver al Menú", fg_color="gray")

        # --- Layout ---
        row_idx = 0
        self.label_salario.grid(row=row_idx, column=0, padx=10, pady=(10, 5), sticky="w")
        self.entry_salario.grid(row=row_idx, column=1, padx=10, pady=(10, 5), sticky="ew"); row_idx += 1

        self.label_inicio.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.date_entry_inicio.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew"); row_idx += 1

        self.label_fin.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.date_entry_fin.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew"); row_idx += 1

        self.calculate_button.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=10, sticky="ew"); row_idx += 1

        # Layout resultados
        self.result_s1_label.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(5, 0), sticky="ew"); row_idx += 1
        self.result_s2_label.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(0, 0), sticky="ew"); row_idx += 1
        self.result_total_label.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew"); row_idx += 1

        # Layout botón volver
        self.back_button.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(15, 10), sticky="ew")


    def get_inputs(self) -> Dict[str, Any]:
        """Devuelve un diccionario con los valores de entrada."""
        try:
            salario = float(self.entry_salario.get().strip() or 0)
            if salario <= 0: raise ValueError("Salario debe ser mayor a cero.")
        except ValueError:
            raise ValueError("Salario Básico Mensual debe ser un número válido.")
        fecha_inicio = self.date_entry_inicio.get_date()
        fecha_fin = self.date_entry_fin.get_date()
        return {
            "salario_mensual": salario,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

    def update_results(self, results: Dict[str, str]):
        """Actualiza las etiquetas de resultado para Prima."""
        self.result_s1_label_var.set(results.get("prima_s1", "Prima Semestre 1: -"))
        self.result_s2_label_var.set(results.get("prima_s2", "Prima Semestre 2: -"))
        self.result_total_label_var.set(results.get("prima_total", "Prima Total Periodo: -"))
        # Resetear color si es necesario
        # self.result_total_label.configure(text_color=theme.COLOR_SIDEBAR_TEXT)


    def show_error(self, error_msg: str):
        """Muestra un mensaje de error en la etiqueta de resultado total."""
        self.result_s1_label_var.set("") # Limpiar detalles
        self.result_s2_label_var.set("")
        self.result_total_label_var.set(f"Error: {error_msg}")
        # self.result_total_label.configure(text_color=theme.COLOR_ERROR_TEXT) # Color error


    def set_calculate_command(self, command):
        self.calculate_button.configure(command=command)

    def set_back_command(self, command):
        self.back_button.configure(command=command)