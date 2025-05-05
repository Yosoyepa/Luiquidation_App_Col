# src/ui/frames/cesantias_frame.py
import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
import src.ui.theme as theme # Importar theme para colores/fuentes
from typing import Any, Dict, Optional

class CesantiasFrame(ctk.CTkFrame):
    """
    Frame para la interfaz de cálculo de Cesantías e Intereses.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # --- Widgets ---
        self.label_salario = ctk.CTkLabel(self, text="Salario Mensual \n Sin Auxilio de transporte:")
        self.entry_salario = ctk.CTkEntry(self, placeholder_text="Ej: 1300000")

        self.label_inicio = ctk.CTkLabel(self, text="Fecha Inicio:")
        self.date_entry_inicio = DateEntry(
            self, date_pattern='yyyy-mm-dd', locale='es_CO'
        )
        self.date_entry_inicio.config({"borderwidth": 1})

        self.label_fin = ctk.CTkLabel(self, text="Fecha Fin:")
        self.date_entry_fin = DateEntry(
            self, date_pattern='yyyy-mm-dd', locale='es_CO'
        )
        self.date_entry_fin.config({"borderwidth": 1})

        self.calculate_button = ctk.CTkButton(self, text="Calcular Cesantías e Intereses") # Texto botón actualizado

        # Etiqueta para resultado de Cesantías
        self.result_cesantias_label_var = ctk.StringVar(value="Cesantías: -")
        self.result_cesantias_label = ctk.CTkLabel(
            self,
            textvariable=self.result_cesantias_label_var,
            font=ctk.CTkFont(size=13, weight="bold") # Fuente resultado
        )

        # Etiqueta para resultado de Intereses (NUEVA)
        self.result_intereses_label_var = ctk.StringVar(value="Intereses Cesantías: -")
        self.result_intereses_label = ctk.CTkLabel(
            self,
            textvariable=self.result_intereses_label_var,
            font=ctk.CTkFont(size=13, weight="bold") # Fuente resultado
        )

        self.back_button = ctk.CTkButton(self, text="Volver al Menú", fg_color="gray")

        # --- Layout ---
        row_idx = 0
        self.label_salario.grid(row=row_idx, column=0, padx=10, pady=(10, 5), sticky="w"); row_idx += 1
        self.entry_salario.grid(row=row_idx-1, column=1, padx=10, pady=(10, 5), sticky="ew")

        self.label_inicio.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w"); row_idx += 1
        self.date_entry_inicio.grid(row=row_idx-1, column=1, padx=10, pady=5, sticky="ew")

        self.label_fin.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w"); row_idx += 1
        self.date_entry_fin.grid(row=row_idx-1, column=1, padx=10, pady=5, sticky="ew")

        self.calculate_button.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=10, sticky="ew"); row_idx += 1

        # Layout de etiquetas de resultado
        self.result_cesantias_label.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(5, 0), sticky="ew"); row_idx += 1
        self.result_intereses_label.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="ew"); row_idx += 1 # Añadir nueva etiqueta

        # Layout botón volver
        self.back_button.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(15, 10), sticky="ew")

    def get_inputs(self) -> Dict[str, Any]:
        """Devuelve un diccionario con los valores de entrada."""
        # ... (sin cambios en esta función) ...
        try:
            salario = float(self.entry_salario.get().strip() or 0)
        except ValueError:
            raise ValueError("Salario mensual debe ser un número válido.")

        fecha_inicio = self.date_entry_inicio.get_date()
        fecha_fin = self.date_entry_fin.get_date()
        return {
            "salario_mensual": salario,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

    def update_results(self, results: Dict[str, str]):
        """
        Actualiza las etiquetas de resultado para Cesantías e Intereses.
        Espera un diccionario con claves 'cesantias' e 'intereses'.
        Si una clave es 'error', muestra el error en ambas etiquetas.
        """
        if "error" in results:
            error_msg = f"Error: {results['error']}"
            self.result_cesantias_label_var.set(error_msg)
            self.result_intereses_label_var.set("") # Ocultar o poner vacío el de intereses
            # Cambiar color a error (opcional)
            # self.result_cesantias_label.configure(text_color=theme.COLOR_ERROR_TEXT)
            # self.result_intereses_label.configure(text_color=theme.COLOR_ERROR_TEXT)
        else:
            cesantias_txt = results.get("cesantias", "Cesantías: -")
            intereses_txt = results.get("intereses", "Intereses Cesantías: -")
            self.result_cesantias_label_var.set(cesantias_txt)
            self.result_intereses_label_var.set(intereses_txt)
            # Resetear color a normal (opcional)
            # self.result_cesantias_label.configure(text_color=theme.COLOR_SIDEBAR_TEXT)
            # self.result_intereses_label.configure(text_color=theme.COLOR_SIDEBAR_TEXT)


    def set_calculate_command(self, command):
        """Asigna comando al botón Calcular."""
        self.calculate_button.configure(command=command)

    def set_back_command(self, command):
        """Asigna comando al botón Volver."""
        self.back_button.configure(command=command)