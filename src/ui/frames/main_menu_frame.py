# src/ui/frames/main_menu_frame.py
import customtkinter as ctk

class MainMenuFrame(ctk.CTkFrame):
    """
    Frame que muestra el menú principal de la aplicación.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1) # Columna principal se expande
        self.grid_rowconfigure(0, weight=1)    # Fila única se expande verticalmente

        self._create_sidebar()
        self._create_main_content()

    def _create_sidebar(self):
        """Crea la barra lateral de modos."""
        self.sidebar_frame = ctk.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) # Empuja botones hacia arriba

        self.mode_label = ctk.CTkLabel(self.sidebar_frame, text="Modo", font=ctk.CTkFont(size=16, weight="bold"))
        self.mode_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Variable para rastrear el modo seleccionado (opcional para Radiobutton)
        # self.selected_mode = ctk.StringVar(value="Laboral")

        self.button_laboral = ctk.CTkButton(self.sidebar_frame, text="Laboral", command=lambda: self.select_mode("Laboral"))
        self.button_laboral.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.button_civil = ctk.CTkButton(self.sidebar_frame, text="Civil", state="disabled", command=lambda: self.select_mode("Civil")) # Deshabilitado inicialmente
        self.button_civil.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.button_admin = ctk.CTkButton(self.sidebar_frame, text="Administrativo", state="disabled", command=lambda: self.select_mode("Administrativo")) # Deshabilitado
        self.button_admin.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Marcar el modo inicial
        self._update_button_styles("Laboral")

    def _create_main_content(self):
        """Crea el área principal con los botones de herramientas."""
        self.main_content_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(1, weight=1) # Dos columnas de botones

        # --- Sección Herramientas Generales ---
        row_idx = 0
        tools_label = ctk.CTkLabel(self.main_content_frame, text="Herramientas Generales", font=ctk.CTkFont(size=14, weight="bold"))
        tools_label.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="w")
        row_idx += 1

        self.button_calc_dias = ctk.CTkButton(self.main_content_frame, text="Calcular Días (30/360)", height=40)
        self.button_calc_dias.grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
        row_idx += 1

        # --- Sección Prestaciones Sociales ---
        prestaciones_label = ctk.CTkLabel(self.main_content_frame, text="Prestaciones Sociales (Laboral)", font=ctk.CTkFont(size=14, weight="bold"))
        prestaciones_label.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=(15, 5), sticky="w")
        row_idx += 1

        self.button_cesantias = ctk.CTkButton(self.main_content_frame, text="Liquidación de Cesantías", height=40)
        self.button_cesantias.grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")

        self.button_prima = ctk.CTkButton(self.main_content_frame, text="Calcular Prima", state="disabled", height=40) # Deshabilitado
        self.button_prima.grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1

        self.button_vacaciones = ctk.CTkButton(self.main_content_frame, text="Calcular Vacaciones", state="disabled", height=40) # Deshabilitado
        self.button_vacaciones.grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")

        self.button_intereses = ctk.CTkButton(self.main_content_frame, text="Intereses Cesantías", state="disabled", height=40) # Deshabilitado
        self.button_intereses.grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1

        # --- Añadir más secciones e ítems aquí (Indemnizaciones, etc.) ---


    def select_mode(self, mode: str):
        """Actualiza visualmente el modo seleccionado."""
        print(f"Modo seleccionado: {mode}") # Placeholder
        self.current_mode = mode
        self._update_button_styles(mode)
        # Aquí podrías habilitar/deshabilitar botones en el main_content
        # basados en el modo, si fuera necesario en el futuro.

    def _update_button_styles(self, selected_mode: str):
        """Cambia el estilo del botón de modo activo."""
        buttons = {
            "Laboral": self.button_laboral,
            "Civil": self.button_civil,
            "Administrativo": self.button_admin
        }
        for mode, button in buttons.items():
             if button.cget("state") != "disabled": # No cambiar estilo si está deshabilitado
                if mode == selected_mode:
                    button.configure(fg_color=button.cget("hover_color")) # Usar color hover para indicar selección
                else:
                    button.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"]) # Color por defecto


    # Métodos para conectar comandos desde el controlador
    def set_calc_dias_command(self, command):
        self.button_calc_dias.configure(command=command)

    def set_cesantias_command(self, command):
        self.button_cesantias.configure(command=command)

    # Añadir setters para otros botones...