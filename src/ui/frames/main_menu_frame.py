# src/ui/frames/main_menu_frame.py
import customtkinter as ctk
from typing import Callable, Optional
import src.ui.theme as theme # Importar el módulo de tema actualizado

# --- Widget Personalizado ToolCard ---
class ToolCard(ctk.CTkFrame):
    def __init__(self, master, text: str, command: Optional[Callable] = None, state="normal", **kwargs):
        super().__init__(master,
                         fg_color=theme.COLOR_CARD_BG,
                         border_color=theme.COLOR_CARD_BORDER,
                         border_width=1,
                         corner_radius=8,
                         **kwargs)
        
        self.text = text
        self.command = command
        self.state = state  # "normal" o "disabled"

        # Placeholder circular para ícono
        self.icon_placeholder = ctk.CTkFrame(
            self, 
            width=30, 
            height=30, 
            corner_radius=6, 
            fg_color=theme.COLOR_ICON_PLACEHOLDER_BG
        )
        self.icon_placeholder.grid(row=0, column=0, padx=10, pady=10)

        # Etiqueta de texto - Crear CTkFont aquí
        self.label = ctk.CTkLabel(
            self,
            text=text,
            text_color=theme.COLOR_SIDEBAR_TEXT,
            # Crear el objeto CTkFont inline usando la especificación del tema
            font=ctk.CTkFont(
                family=theme.FONT_SPEC_CARD_TEXT[0],
                size=theme.FONT_SPEC_CARD_TEXT[1],
                weight=theme.FONT_SPEC_CARD_TEXT[2]
            ),
            anchor="w"
        )
        self.label.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        
        # Configurar estado
        if state == "disabled":
            self.label.configure(text_color=theme.COLOR_CARD_DISABLED_TEXT)

        # Eventos hover/click si está habilitado
        if state == "normal":
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
            self.bind("<Button-1>", self._on_click)
            self.label.bind("<Button-1>", self._on_click)
            self.icon_placeholder.bind("<Button-1>", self._on_click)

    def _on_enter(self, event=None):
        if self.state == "normal":
            self.configure(fg_color=theme.COLOR_CARD_HOVER)

    def _on_leave(self, event=None):
        if self.state == "normal":
            self.configure(fg_color=theme.COLOR_CARD_BG)
            
    def _on_click(self, event=None):
        if self.state == "normal" and self.command:
            # Efecto visual al hacer click
            self.configure(fg_color=theme.COLOR_CARD_CLICK)
            self.after(100, lambda: self.configure(fg_color=theme.COLOR_CARD_BG))
            # Ejecutar comando
            self.command()


# --- Clase Principal del Frame del Menú ---
class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Set explicit white background for the main frame
        kwargs.update({"fg_color": "#FFFFFF"})  # Using white color directly
        super().__init__(master, **kwargs)
        
        # Inicialización de variables
        self.cards_main = {}  # Diccionario para almacenar las tarjetas
        self.buttons_sidebar = {}  # Diccionario para almacenar botones
        self.current_mode = "Laboral"  # Modo por defecto
        
        # Configuración del grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Crear componentes UI
        self._create_sidebar()
        self._create_main_content()

    def _create_sidebar(self):
        """Crea la barra lateral de modos."""
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0, fg_color=theme.COLOR_SIDEBAR_BG)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Título "Liquidaciones" - Crear CTkFont aquí
        self.mode_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Liquidaciones",
            text_color=theme.COLOR_SIDEBAR_TEXT,
            # Crear el objeto CTkFont inline
            font=ctk.CTkFont(
                family=theme.FONT_SPEC_SIDEBAR_TITLE[0],
                size=theme.FONT_SPEC_SIDEBAR_TITLE[1],
                weight=theme.FONT_SPEC_SIDEBAR_TITLE[2]
            ),
            anchor="w"
        )
        self.mode_label.grid(row=0, column=0, padx=15, pady=(20, 15), sticky="w")

        # Botones de Modo - Crear CTkFont aquí para el estado inicial
        modes = ["Laboral", "Civil", "Administrativo"]
        initial_font = ctk.CTkFont(
                family=theme.FONT_SPEC_SIDEBAR_NORMAL[0],
                size=theme.FONT_SPEC_SIDEBAR_NORMAL[1],
                weight=theme.FONT_SPEC_SIDEBAR_NORMAL[2]
            )
        for i, mode in enumerate(modes):
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=mode,
                text_color=theme.COLOR_SIDEBAR_TEXT,
                fg_color="transparent",
                hover=False,
                anchor="w",
                font=initial_font, # Usar fuente inicial
                command=lambda m=mode: self.select_mode(m),
                corner_radius=0
            )
            button.grid(row=i + 1, column=0, padx=0, pady=0, sticky="ew")
            self.buttons_sidebar[mode] = button
            if mode != "Laboral":
                 button.configure(state="disabled", text_color=theme.COLOR_SIDEBAR_DISABLED_TEXT)

        self.select_mode(self.current_mode, initial_load=True)

    def _create_main_content(self):
        """Crea el área principal con las tarjetas de herramientas."""
        self.main_content_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=4,
            fg_color="transparent",
            scrollbar_fg_color=theme.COLOR_SCROLLBAR_FG,
            scrollbar_button_color=theme.COLOR_SCROLLBAR_FG,
            scrollbar_button_hover_color=theme.COLOR_SCROLLBAR_HOVER
            )
        self.main_content_frame.grid(row=0, column=1, padx=20, pady=15, sticky="nsew")
        self.main_content_frame.grid_columnconfigure(0, weight=1, uniform="card_col")
        self.main_content_frame.grid_columnconfigure(1, weight=1, uniform="card_col")

        row_idx = 0
        # Crear fuente para headers inline
        header_font = ctk.CTkFont(
                family=theme.FONT_SPEC_SECTION_HEADER[0],
                size=theme.FONT_SPEC_SECTION_HEADER[1],
                weight=theme.FONT_SPEC_SECTION_HEADER[2]
            )

        # --- Sección Herramientas Generales ---
        tools_label = ctk.CTkLabel(self.main_content_frame, text="Herramientas Generales", text_color=theme.COLOR_SECTION_HEADER, font=header_font)
        tools_label.grid(row=row_idx, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="w")
        row_idx += 1
        # ToolCard crea su propia fuente internamente ahora
        self.cards_main["CalcDias"] = ToolCard(self.main_content_frame, text="Calcular Días (30/360)")
        self.cards_main["CalcDias"].grid(row=row_idx, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        row_idx += 1

        # --- Sección Prestaciones Sociales ---
        prestaciones_label = ctk.CTkLabel(self.main_content_frame, text="Prestaciones Sociales", text_color=theme.COLOR_SECTION_HEADER, font=header_font)
        prestaciones_label.grid(row=row_idx, column=0, columnspan=2, padx=5, pady=(15, 5), sticky="w")
        row_idx += 1
        # ... (Instanciación de ToolCards) ...
        self.cards_main["Cesantias"] = ToolCard(self.main_content_frame, text="Liquidación de Cesantías")
        self.cards_main["Cesantias"].grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
        self.cards_main["Vacaciones"] = ToolCard(self.main_content_frame, text="Calcular Vacaciones", state="disabled")
        self.cards_main["Vacaciones"].grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1
        self.cards_main["Prima"] = ToolCard(self.main_content_frame, text="Calcular Prima", state="disabled")
        self.cards_main["Prima"].grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
        self.cards_main["Intereses"] = ToolCard(self.main_content_frame, text="Calcular Intereses a Cesantías", state="normal")
        self.cards_main["Intereses"].grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1

        # --- Sección Indemnizaciones por Despidos ---
        indem_label = ctk.CTkLabel(self.main_content_frame, text="Indemnizaciones por Despidos", text_color=theme.COLOR_SECTION_HEADER, font=header_font)
        indem_label.grid(row=row_idx, column=0, columnspan=2, padx=5, pady=(15, 5), sticky="w")
        row_idx += 1
        # ... (Instanciación de ToolCards) ...
        self.cards_main["IndemSinCausa"] = ToolCard(self.main_content_frame, text="Despido sin Justa Causa", state="disabled")
        self.cards_main["IndemSinCausa"].grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
        self.cards_main["IndemConCausa"] = ToolCard(self.main_content_frame, text="Despido con Justa Causa", state="disabled")
        self.cards_main["IndemConCausa"].grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
        row_idx += 1

        # --- Sección Horas Extras / Recargos ---
        horas_label = ctk.CTkLabel(self.main_content_frame, text="Horas Extras / Recargos", text_color=theme.COLOR_SECTION_HEADER, font=header_font)
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
        if not initial_load and self.current_mode == mode:
             return

        if not initial_load:
            print(f"Cambiando a modo: {mode}")
        self.current_mode = mode

        # Crear los objetos CTkFont necesarios aquí, justo antes de usarlos
        font_normal = ctk.CTkFont(
            family=theme.FONT_SPEC_SIDEBAR_NORMAL[0],
            size=theme.FONT_SPEC_SIDEBAR_NORMAL[1],
            weight=theme.FONT_SPEC_SIDEBAR_NORMAL[2]
        )
        font_selected = ctk.CTkFont(
            family=theme.FONT_SPEC_SIDEBAR_SELECTED[0],
            size=theme.FONT_SPEC_SIDEBAR_SELECTED[1],
            weight=theme.FONT_SPEC_SIDEBAR_SELECTED[2]
        )

        # Actualizar estilos de botones del sidebar
        for btn_mode, button in self.buttons_sidebar.items():
             if button.cget("state") != "disabled":
                if btn_mode == mode:
                    # --- Estilo Seleccionado ---
                    button.configure(
                        fg_color=theme.COLOR_SIDEBAR_SELECTED_BG,
                        text_color=theme.COLOR_SIDEBAR_SELECTED_TEXT, # Blanco
                        font=font_selected # Fuente seleccionada (más grande/bold)
                    )
                else:
                    # --- Estilo No Seleccionado ---
                    button.configure(
                        fg_color="transparent",
                        text_color=theme.COLOR_SIDEBAR_TEXT, # Texto normal oscuro
                        font=font_normal # Fuente normal
                    )

    # --- Métodos para conectar comandos (sin cambios) ---
    def set_card_command(self, card_key: str, command: Callable):
        # ... (sin cambios en este método) ...
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