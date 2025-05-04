# src/ui/frames/main_menu_frame.py
import customtkinter as ctk
from typing import Callable, Optional
import src.ui.theme as theme # <--- Importar el módulo de tema

# --- Widget Personalizado para Tarjetas de Herramientas ---
class ToolCard(ctk.CTkFrame):
    """
    Widget personalizado que representa una tarjeta clickeable para una herramienta.
    """
    def __init__(self, master, text: str, command: Optional[Callable] = None, state="normal", **kwargs):
        super().__init__(master,
                         fg_color=theme.COLOR_CARD_BG, # <--- Usar theme.COLOR_...
                         border_color=theme.COLOR_CARD_BORDER,
                         border_width=1,
                         corner_radius=8, # Podría ser theme.CORNER_RADIUS_CARD
                         **kwargs)

        self.command = command
        self.state = state
        self.hover_color = theme.COLOR_CARD_HOVER # <--- Usar theme.COLOR_...

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Placeholder para el ícono
        self.icon_placeholder = ctk.CTkFrame(
            self,
            width=40,
            height=40,
            fg_color=theme.COLOR_ICON_PLACEHOLDER_BG, # <--- Usar theme.COLOR_...
            corner_radius=6 # Podría ser theme.CORNER_RADIUS_ICON
        )
        self.icon_placeholder.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") # Podría ser theme.PADDING_DEFAULT

        # Etiqueta de texto
        self.label = ctk.CTkLabel(
            self,
            text=text,
            text_color=theme.COLOR_SIDEBAR_TEXT, # <--- Usar theme.COLOR_...
            font=ctk.CTkFont(size=12), # Podría ser theme.FONT_SIZE_NORMAL
            anchor="w"
        )
        self.label.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        # Vincular eventos (sin cambios aquí, pero usa colores del theme)
        if self.state == "normal" and self.command:
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
            self.bind("<Button-1>", self._on_click)
            self.label.bind("<Button-1>", self._on_click)
            self.icon_placeholder.bind("<Button-1>", self._on_click)
        elif self.state == "disabled":
             self.label.configure(text_color=theme.COLOR_CARD_DISABLED_TEXT) # <--- Usar theme.COLOR_...


    def _on_enter(self, event=None):
        if self.state == "normal":
            self.configure(fg_color=self.hover_color)

    def _on_leave(self, event=None):
        if self.state == "normal":
            self.configure(fg_color=theme.COLOR_CARD_BG) # <--- Usar theme.COLOR_...

    def _on_click(self, event=None):
        if self.state == "normal" and self.command:
            self.command()
            self.configure(fg_color=theme.COLOR_CARD_CLICK) # <--- Usar theme.COLOR_...
            self.after(100, lambda: self.configure(fg_color=self.hover_color))

    def configure(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs["state"]
            if self.state == "disabled":
                self.label.configure(text_color=theme.COLOR_CARD_DISABLED_TEXT) # <--- Usar theme.COLOR_...
                self.unbind("<Enter>")
                self.unbind("<Leave>")
                self.unbind("<Button-1>")
                self.label.unbind("<Button-1>")
                self.icon_placeholder.unbind("<Button-1>")
            elif self.state == "normal":
                self.label.configure(text_color=theme.COLOR_SIDEBAR_TEXT) # <--- Usar theme.COLOR_...
                if self.command:
                    self.bind("<Enter>", self._on_enter)
                    self.bind("<Leave>", self._on_leave)
                    self.bind("<Button-1>", self._on_click)
                    self.label.bind("<Button-1>", self._on_click)
                    self.icon_placeholder.bind("<Button-1>", self._on_click)

        super().configure(**kwargs)


# --- Clase Principal del Frame del Menú ---
class MainMenuFrame(ctk.CTkFrame):
    """
    Frame que muestra el menú principal de la aplicación, rediseñado.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.COLOR_MAIN_BG, **kwargs) # <--- Usar theme.COLOR_...

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buttons_sidebar = {}
        self.cards_main = {}
        self.current_mode = "Laboral"

        self._create_sidebar()
        self._create_main_content()

    def _create_sidebar(self):
        """Crea la barra lateral de modos."""
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0, fg_color=theme.COLOR_SIDEBAR_BG) # <--- Usar theme.COLOR_...
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.mode_label = ctk.CTkLabel(self.sidebar_frame, text="Liquidaciones", text_color=theme.COLOR_SIDEBAR_TEXT, font=ctk.CTkFont(size=16, weight="bold")) # <--- Usar theme.COLOR_...
        self.mode_label.grid(row=0, column=0, padx=20, pady=(20, 15))

        modes = ["Laboral", "Civil", "Administrativo"]
        for i, mode in enumerate(modes):
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=mode,
                text_color=theme.COLOR_SIDEBAR_TEXT, # <--- Usar theme.COLOR_...
                fg_color="transparent",
                hover=False,
                anchor="w",
                font=ctk.CTkFont(size=13),
                command=lambda m=mode: self.select_mode(m)
            )
            button.grid(row=i + 1, column=0, padx=15, pady=8, sticky="ew")
            self.buttons_sidebar[mode] = button
            if mode != "Laboral":
                 button.configure(state="disabled", text_color=theme.COLOR_SIDEBAR_DISABLED_TEXT) # <--- Usar theme.COLOR_...

        self.select_mode(self.current_mode, initial_load=True)


    def _create_main_content(self):
        """Crea el área principal con las tarjetas de herramientas."""
        self.main_content_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=1, padx=20, pady=15, sticky="nsew")
        self.main_content_frame.grid_columnconfigure(0, weight=1, uniform="card_col")
        self.main_content_frame.grid_columnconfigure(1, weight=1, uniform="card_col")

        row_idx = 0

        # --- Sección Herramientas Generales ---
        tools_label = ctk.CTkLabel(self.main_content_frame, text="Herramientas Generales", text_color=theme.COLOR_SECTION_HEADER, font=ctk.CTkFont(size=14, weight="bold")) # <--- Usar theme.COLOR_...
        tools_label.grid(row=row_idx, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="w")
        row_idx += 1
        self.cards_main["CalcDias"] = ToolCard(self.main_content_frame, text="Calcular Días (30/360)")
        self.cards_main["CalcDias"].grid(row=row_idx, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        row_idx += 1

        # --- Sección Prestaciones Sociales ---
        prestaciones_label = ctk.CTkLabel(self.main_content_frame, text="Prestaciones Sociales", text_color=theme.COLOR_SECTION_HEADER, font=ctk.CTkFont(size=14, weight="bold")) # <--- Usar theme.COLOR_...
        prestaciones_label.grid(row=row_idx, column=0, columnspan=2, padx=5, pady=(15, 5), sticky="w")
        row_idx += 1
        # ... (Instanciación de ToolCards usando theme.COLOR_... internamente) ...
        self.cards_main["Cesantias"] = ToolCard(self.main_content_frame, text="Liquidación de Cesantías")
        self.cards_main["Cesantias"].grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
        self.cards_main["Vacaciones"] = ToolCard(self.main_content_frame, text="Calcular Vacaciones", state="disabled")
        self.cards_main["Vacaciones"].grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1
        self.cards_main["Prima"] = ToolCard(self.main_content_frame, text="Calcular Prima", state="disabled")
        self.cards_main["Prima"].grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
        self.cards_main["Intereses"] = ToolCard(self.main_content_frame, text="Calcular Intereses a Cesantías", state="disabled")
        self.cards_main["Intereses"].grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1

        # --- Sección Indemnizaciones por Despidos ---
        indem_label = ctk.CTkLabel(self.main_content_frame, text="Indemnizaciones por Despidos", text_color=theme.COLOR_SECTION_HEADER, font=ctk.CTkFont(size=14, weight="bold")) # <--- Usar theme.COLOR_...
        indem_label.grid(row=row_idx, column=0, columnspan=2, padx=5, pady=(15, 5), sticky="w")
        row_idx += 1
        # ... (Instanciación de ToolCards) ...
        self.cards_main["IndemSinCausa"] = ToolCard(self.main_content_frame, text="Despido sin Justa Causa", state="disabled")
        self.cards_main["IndemSinCausa"].grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
        self.cards_main["IndemConCausa"] = ToolCard(self.main_content_frame, text="Despido con Justa Causa", state="disabled")
        self.cards_main["IndemConCausa"].grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1

        # --- Sección Horas Extras / Recargos ---
        horas_label = ctk.CTkLabel(self.main_content_frame, text="Horas Extras / Recargos", text_color=theme.COLOR_SECTION_HEADER, font=ctk.CTkFont(size=14, weight="bold")) # <--- Usar theme.COLOR_...
        horas_label.grid(row=row_idx, column=0, columnspan=2, padx=5, pady=(15, 5), sticky="w")
        row_idx += 1
        # ... (Instanciación de ToolCards) ...
        self.cards_main["HorasExtras"] = ToolCard(self.main_content_frame, text="Horas Extras", state="disabled")
        self.cards_main["HorasExtras"].grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
        self.cards_main["Recargos"] = ToolCard(self.main_content_frame, text="Recargos Nocturnos / Dominicales", state="disabled")
        self.cards_main["Recargos"].grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1


    def select_mode(self, mode: str, initial_load=False):
        """Actualiza visualmente el modo seleccionado en la barra lateral."""
        if not initial_load:
            print(f"Modo seleccionado: {mode}")
        self.current_mode = mode
        for btn_mode, button in self.buttons_sidebar.items():
             if button.cget("state") != "disabled":
                if btn_mode == mode:
                    button.configure(fg_color=theme.COLOR_SIDEBAR_SELECTED_BG, text_color=theme.COLOR_SIDEBAR_SELECTED_TEXT) # <--- Usar theme.COLOR_...
                else:
                    button.configure(fg_color="transparent", text_color=theme.COLOR_SIDEBAR_TEXT) # <--- Usar theme.COLOR_...

    # --- Métodos para conectar comandos desde el controlador a las TARJETAS ---
    def set_card_command(self, card_key: str, command: Callable):
        """Asigna un comando a una tarjeta específica usando su clave."""
        card = self.cards_main.get(card_key)
        if card:
            card.command = command
            if card.state == "normal":
                 card.bind("<Enter>", card._on_enter)
                 card.bind("<Leave>", card._on_leave)
                 card.bind("<Button-1>", card._on_click)
                 card.label.bind("<Button-1>", card._on_click)
                 card.icon_placeholder.bind("<Button-1>", card._on_click)
        else:
            print(f"Advertencia: No se encontró la tarjeta con clave '{card_key}'")