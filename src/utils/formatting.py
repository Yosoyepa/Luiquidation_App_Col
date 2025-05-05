"""
Utilidades para formateo de valores en la aplicación.
"""
import locale
from typing import Optional

def formatear_moneda(valor: float, simbolo: str = "COP") -> str:
    """
    Formatea un valor numérico como moneda.
    
    Args:
        valor: Valor a formatear
        simbolo: Símbolo de moneda a usar
        
    Returns:
        String formateado como moneda
    """
    try:
        return locale.currency(valor, grouping=True, symbol=f'{simbolo} ')
    except (ValueError, locale.Error):
        # Fallback si locale falla
        return f"{simbolo} {valor:,.2f}"

def formatear_porcentaje(valor: float, decimales: int = 2) -> str:
    """
    Formatea un valor numérico como porcentaje.
    
    Args:
        valor: Valor a formatear (ej: 0.12 para 12%)
        decimales: Número de decimales a mostrar
        
    Returns:
        String formateado como porcentaje
    """
    return f"{valor * 100:.{decimales}f}%"