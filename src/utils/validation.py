"""
Utilidades de validación para la aplicación de liquidación.
Contiene funciones para validar entradas de usuario y datos.
"""
import datetime
from typing import Optional, Tuple, Union, Any

def validar_fecha(fecha: Any) -> Tuple[bool, Optional[str]]:
    """
    Valida si el valor es una fecha válida.
    
    Args:
        fecha: El valor a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not isinstance(fecha, datetime.date):
        return False, "El valor debe ser una fecha válida"
    return True, None

def validar_fechas_periodo(fecha_inicio: datetime.date, fecha_fin: datetime.date) -> Tuple[bool, Optional[str]]:
    """
    Valida si las fechas de inicio y fin forman un periodo válido.
    
    Args:
        fecha_inicio: Fecha de inicio del periodo
        fecha_fin: Fecha de fin del periodo
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if fecha_fin < fecha_inicio:
        return False, "La fecha de fin no puede ser anterior a la fecha de inicio"
    return True, None

def validar_valor_numerico(valor: Any, min_valor: float = 0, campo: str = "valor") -> Tuple[bool, Optional[str]]:
    """
    Valida si el valor es un número y está dentro del rango permitido.
    
    Args:
        valor: El valor a validar
        min_valor: Valor mínimo permitido
        campo: Nombre del campo para el mensaje de error
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    try:
        numero = float(str(valor).strip().replace(',', '').replace('$', ''))
        if numero < min_valor:
            return False, f"El {campo} debe ser mayor o igual a {min_valor}"
        return True, None
    except (ValueError, TypeError):
        return False, f"El {campo} debe ser un número válido"