# src/ui/theme.py
# -*- coding: utf-8 -*-

"""
theme.py

Define las constantes de estilo visual (colores, fuentes, etc.)
para la interfaz de usuario de la aplicación.
"""

from typing import Final

# --- Paleta de Colores Principal---

COLOR_SIDEBAR_BG: Final[str] = "#F2EBF9"         # Lila muy claro (Sidebar background)
COLOR_SIDEBAR_TEXT: Final[str] = "#333333"         # Gris oscuro/Negro (Texto general)
COLOR_SIDEBAR_SELECTED_BG: Final[str] = "#E8DDF5" # Lila un poco más oscuro (Selección en Sidebar)
COLOR_SIDEBAR_SELECTED_TEXT: Final[str] = "#333333" # Texto oscuro para ítem seleccionado
COLOR_SIDEBAR_DISABLED_TEXT: Final[str] = "#9B9B9B" # Gris claro para texto deshabilitado

COLOR_MAIN_BG: Final[str] = "#FFFFFF"             # Blanco (Fondo área principal)

COLOR_CARD_BG: Final[str] = "#FFFFFF"             # Blanco (Fondo tarjetas/botones)
COLOR_CARD_BORDER: Final[str] = "#EAEAEA"         # Gris muy claro (Borde tarjetas)
COLOR_CARD_HOVER: Final[str] = "#F8F8F8"          # Gris extra claro (Hover en tarjetas)
COLOR_CARD_CLICK: Final[str] = "#E0E0E0"          # Gris claro (Efecto visual al clickear tarjeta)
COLOR_CARD_DISABLED_TEXT: Final[str] = "#BDBDBD"  # Gris medio (Texto en tarjeta deshabilitada)

COLOR_ICON_PLACEHOLDER_BG: Final[str] = "#F2EBF9" # Lila claro (Fondo placeholder icono)

COLOR_SECTION_HEADER: Final[str] = "#4A4A4A"      # Gris oscuro (Títulos de sección)

COLOR_BUTTON_TEXT: Final[str] = "#FFFFFF"          # Blanco (Texto en botones estándar CTk)
COLOR_BUTTON_BORDER: Final[str] = "#C0C0C0"       # Gris para borde de botón por defecto (ejemplo)

COLOR_ERROR_TEXT: Final[str] = "#B00020"          # Rojo para mensajes de error (ejemplo)
COLOR_SUCCESS_TEXT: Final[str] = "#006400"       # Verde para mensajes de éxito (ejemplo)

# --- Fuentes (Opcional - Podrías definir fuentes estándar aquí también) ---
# FONT_FAMILY_DEFAULT: Final[str] = "Segoe UI"
# FONT_SIZE_NORMAL: Final[int] = 12
# FONT_SIZE_HEADER: Final[int] = 14
# FONT_WEIGHT_BOLD: Final[str] = "bold"

# --- Otros Estilos (Padding, Corner Radius - Opcional) ---
# PADDING_DEFAULT: Final[int] = 10
# CORNER_RADIUS_CARD: Final[int] = 8
# CORNER_RADIUS_ICON: Final[int] = 6