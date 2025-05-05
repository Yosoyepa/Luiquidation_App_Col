# src/ui/frames/intereses_cesantias_frame.py
import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
import src.ui.theme as theme
from typing import Dict, Any

class InteresesCesantiasFrame(ctk.CTkFrame):
    """
    Frame para la interfaz de cálculo de Intereses sobre Cesantías.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # --- Widgets ---
        # CAMBIO: Pide el valor de las cesantías, no el salario
        self.label_cesantias = ctk.CTkLabel(self, text="Valor Cesantías ($):")
        self.entry_cesantias = ctk.CTkEntry(self, placeholder_text="Ej: 1440606")

        self.label_inicio = ctk.CTkLabel(self, text="Fecha Inicio Periodo:")
        self.date_entry_inicio = DateEntry(self, date_pattern='yyyy-mm-dd', locale='es_CO')
        self.date_entry_inicio.config({"borderwidth": 1})

        self.label_fin = ctk.CTkLabel(self, text="Fecha Fin Periodo:")
        self.date_entry_fin = DateEntry(self, date_pattern='yyyy-mm-dd', locale='es_CO')
        self.date_entry_fin.config({"borderwidth": 1})

        self.calculate_button = ctk.CTkButton(self, text="Calcular Intereses")

        # Etiqueta para resultado de Intereses
        self.result_intereses_label_var = ctk.StringVar(value="Intereses Calculados: -")
        self.result_intereses_label = ctk.CTkLabel(
            self,
            textvariable=self.result_intereses_label_var,
             font=ctk.CTkFont( # Crear fuente inline
                 family=theme.FONT_FAMILY_DEFAULT,
                 size=13, weight="bold"
            )
        )

        self.back_button = ctk.CTkButton(self, text="Volver al Menú", fg_color="gray")

        # --- Layout ---
        row_idx = 0
        self.label_cesantias.grid(row=row_idx, column=0, padx=10, pady=(10, 5), sticky="w")
        self.entry_cesantias.grid(row=row_idx, column=1, padx=10, pady=(10, 5), sticky="ew"); row_idx += 1

        self.label_inicio.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.date_entry_inicio.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew"); row_idx += 1

        self.label_fin.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.date_entry_fin.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew"); row_idx += 1

        self.calculate_button.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=10, sticky="ew"); row_idx += 1

        self.result_intereses_label.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="ew"); row_idx += 1

        self.back_button.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(15, 10), sticky="ew")

    def get_inputs(self) -> Dict[str, Any]:
        """Devuelve un diccionario con los valores de entrada."""
        try:
            # Obtener valor cesantías del entry
            valor_cesantias_str = self.entry_cesantias.get().strip().replace('COP', '').replace(',', '').replace('$', '')
            valor_cesantias = float(valor_cesantias_str or 0)
            if valor_cesantias < 0: raise ValueError("Valor Cesantías no puede ser negativo.")
        except ValueError:
            raise ValueError("Valor Cesantías debe ser un número válido.")

        fecha_inicio = self.date_entry_inicio.get_date()
        fecha_fin = self.date_entry_fin.get_date()
        return {
            "valor_cesantias": valor_cesantias,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

    def update_result(self, result_text: str):
        """Actualiza la etiqueta de resultado para Intereses."""
        self.result_intereses_label_var.set(result_text)
        # Resetear color
        # self.result_intereses_label.configure(text_color=theme.COLOR_SIDEBAR_TEXT)

    def show_error(self, error_msg: str):
        """Muestra un mensaje de error en la etiqueta de resultado."""
        self.result_intereses_label_var.set(f"Error: {error_msg}")
        # Cambiar color (opcional)
        # self.result_intereses_label.configure(text_color=theme.COLOR_ERROR_TEXT)

    def set_calculate_command(self, command):
        self.calculate_button.configure(command=command)

    def set_back_command(self, command):
        self.back_button.configure(command=command)