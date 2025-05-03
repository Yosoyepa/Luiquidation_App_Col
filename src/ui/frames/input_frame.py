# src/ui/frames/input_frame.py
import customtkinter as ctk
from tkcalendar import DateEntry
import datetime

class InputFrame(ctk.CTkFrame):
    """
    Frame que contiene los widgets para la entrada de fechas y el botón de cálculo.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1) # Columna de widgets se expande

        # --- Widgets ---
        self.label_inicio = ctk.CTkLabel(self, text="Fecha Inicio:")
        self.date_entry_inicio = DateEntry(
            self,
            date_pattern='yyyy-mm-dd', # Formato de fecha
            selectmode='day',
            showweeknumbers=False,
            locale='es_CO' # Para que muestre calendario en español si está instalado locale
        )
        # Estilo básico para DateEntry (puedes personalizar más si lo necesitas)
        self.date_entry_inicio.config({"borderwidth": 1})


        self.label_fin = ctk.CTkLabel(self, text="Fecha Fin:")
        self.date_entry_fin = DateEntry(
            self,
            date_pattern='yyyy-mm-dd',
            selectmode='day',
            showweeknumbers=False,
            locale='es_CO'
        )
        self.date_entry_fin.config({"borderwidth": 1})

        self.calculate_button = ctk.CTkButton(self, text="Calcular Días")

        # --- Layout ---
        self.label_inicio.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.date_entry_inicio.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")

        self.label_fin.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.date_entry_fin.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

    def get_fecha_inicio(self) -> datetime.date:
        """Devuelve la fecha de inicio seleccionada como objeto date."""
        return self.date_entry_inicio.get_date()

    def get_fecha_fin(self) -> datetime.date:
        """Devuelve la fecha de fin seleccionada como objeto date."""
        return self.date_entry_fin.get_date()

    def set_button_command(self, command):
        """Asigna un comando al botón Calcular."""
        self.calculate_button.configure(command=command)