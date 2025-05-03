# src/ui/frames/cesantias_frame.py
import customtkinter as ctk
from tkcalendar import DateEntry
import datetime

class CesantiasFrame(ctk.CTkFrame):
    """
    Frame para la interfaz de cálculo de Cesantías.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # --- Widgets ---
        self.label_salario = ctk.CTkLabel(self, text="Salario Mensual:")
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

        # Checkbox Auxilio (Opcional - podría ser automático)
        # self.check_auxilio_var = ctk.StringVar(value="on") # Ejemplo si fuera manual
        # self.check_auxilio = ctk.CTkCheckBox(self, text="¿Determinar Automáticamente Aux. Transporte?", variable=self.check_auxilio_var, onvalue="on", offvalue="off")
        # self.check_auxilio.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.calculate_button = ctk.CTkButton(self, text="Calcular Cesantías")
        self.result_label_var = ctk.StringVar(value="Cesantías: -")
        self.result_label = ctk.CTkLabel(self, textvariable=self.result_label_var, font=ctk.CTkFont(size=13))

        self.back_button = ctk.CTkButton(self, text="Volver al Menú", fg_color="gray")

        # --- Layout ---
        self.label_salario.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.entry_salario.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")

        self.label_inicio.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.date_entry_inicio.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.label_fin.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.date_entry_fin.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.back_button.grid(row=6, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="ew")


    def get_inputs(self) -> dict:
        """Devuelve un diccionario con los valores de entrada."""
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

    def update_result(self, text: str):
        """Actualiza la etiqueta de resultado."""
        self.result_label_var.set(text)

    def set_calculate_command(self, command):
        """Asigna comando al botón Calcular."""
        self.calculate_button.configure(command=command)

    def set_back_command(self, command):
        """Asigna comando al botón Volver."""
        self.back_button.configure(command=command)