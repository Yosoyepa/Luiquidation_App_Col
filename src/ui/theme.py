# src/ui/theme.py
# -*- coding: utf-8 -*-

"""
theme.py

Define las constantes de estilo visual (colores, fuentes, etc.)
para la interfaz de usuario de la aplicación.
"""

from typing import Final, Tuple, Dict, Any

# --- Paleta de Colores Principal (Ajustada por el usuario) ---
COLOR_SIDEBAR_BG: Final[str] = "#F0D7F9"         # Lila muy claro (Sidebar background)
COLOR_SIDEBAR_TEXT: Final[str] = "#333333"         # Gris oscuro/Negro (Texto general Sidebar)
COLOR_SIDEBAR_SELECTED_BG: Final[str] = "#CEAECA" # Lila más oscuro (Selección en Sidebar)
COLOR_SIDEBAR_SELECTED_TEXT: Final[str] = "#FFFFFF" # BLANCO (Texto ítem seleccionado Sidebar)
COLOR_SIDEBAR_DISABLED_TEXT: Final[str] = "#9B9B9B" # Gris claro (Texto deshabilitado Sidebar)

COLOR_MAIN_BG: Final[str] = "#FFFFFF"             # Blanco (Fondo área principal)

COLOR_CARD_BG: Final[str] = "#FFFFFF"             # Blanco (Fondo tarjetas/botones)
COLOR_CARD_BORDER: Final[str] = "#EAEAEA"         # Gris muy claro (Borde tarjetas)
COLOR_CARD_HOVER: Final[str] = "#F8F8F8"          # Gris extra claro (Hover en tarjetas)
COLOR_CARD_CLICK: Final[str] = "#E0E0E0"          # Gris claro (Efecto visual al clickear tarjeta)
COLOR_CARD_DISABLED_TEXT: Final[str] = "#BDBDBD"  # Gris medio (Texto en tarjeta deshabilitada)

COLOR_ICON_PLACEHOLDER_BG: Final[str] = "#F0D7F9" # Lila claro (Fondo placeholder icono)

COLOR_SECTION_HEADER: Final[str] = "#4A4A4A"      # Gris oscuro (Títulos de sección)

COLOR_SCROLLBAR_FG: Final[str] = "#FFFFFF"        # Gris claro para la barra scroll
COLOR_SCROLLBAR_HOVER: Final[str] = "#DBDBDB"     # Gris un poco más oscuro para hover scroll

COLOR_BUTTON_TEXT: Final[str] = "#FFFFFF"
COLOR_BUTTON_BORDER: Final[str] = "#C0C0C0"
COLOR_ERROR_TEXT: Final[str] = "#B00020"
COLOR_SUCCESS_TEXT: Final[str] = "#006400"

# --- Especificaciones de Fuentes ---
# Definimos las propiedades, NO el objeto CTkFont aquí
FONT_FAMILY_DEFAULT: Final[str] = "Inter" # O la fuente que prefieras/tengas

# Especificación: (family, size, weight)
FONT_SPEC_SIDEBAR_TITLE: Final[Tuple[str, int, str]] = (FONT_FAMILY_DEFAULT, 16, "bold")
FONT_SPEC_SIDEBAR_NORMAL: Final[Tuple[str, int, str]] = (FONT_FAMILY_DEFAULT, 13, "normal")
FONT_SPEC_SIDEBAR_SELECTED: Final[Tuple[str, int, str]] = (FONT_FAMILY_DEFAULT, 14, "bold")
FONT_SPEC_SECTION_HEADER: Final[Tuple[str, int, str]] = (FONT_FAMILY_DEFAULT, 14, "bold")
FONT_SPEC_CARD_TEXT: Final[Tuple[str, int, str]] = (FONT_FAMILY_DEFAULT, 12, "normal")

# Podrías añadir más especificaciones aquí...