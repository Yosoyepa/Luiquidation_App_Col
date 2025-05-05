"""
Utilidades para el manejo de fechas en la aplicación.
"""
import datetime
from typing import Optional, Tuple

def obtener_anio_actual() -> int:
    """Retorna el año actual."""
    return datetime.datetime.now().year

def formatear_fecha(fecha: datetime.date) -> str:
    """
    Formatea una fecha en formato DD/MM/YYYY.
    
    Args:
        fecha: Fecha a formatear
        
    Returns:
        Fecha formateada como string
    """
    return fecha.strftime("%d/%m/%Y")

def calcular_dias_liquidacion(fecha_inicio: datetime.date, fecha_fin: datetime.date) -> int:
    """
    Calcula el número de días entre dos fechas para fines de liquidación laboral
    en Colombia, utilizando la convención de año de 360 días y mes de 30 días.

    Reglas aplicadas:
    1. Se considera que todos los meses tienen 30 días.
    2. Si el día de inicio es 31, se toma como 30 para el cálculo.
    3. Si el día de fin es 31, se toma como 30 para el cálculo.
    4. El cálculo incluye tanto la fecha de inicio como la fecha de fin (es inclusivo),
       sumando 1 al resultado de la diferencia calculada con la fórmula 30/360.

    Args:
        fecha_inicio: La fecha de inicio del periodo (objeto datetime.date).
        fecha_fin: La fecha de fin del periodo (objeto datetime.date).

    Returns:
        El número de días de liquidación calculados (int).

    Raises:
        ValueError: Si la fecha_fin es anterior a la fecha_inicio.
    """
    if fecha_fin < fecha_inicio:
        raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio.")

    # Extraer componentes de las fechas
    y1, m1, d1 = fecha_inicio.year, fecha_inicio.month, fecha_inicio.day
    y2, m2, d2 = fecha_fin.year, fecha_fin.month, fecha_fin.day

    # Aplicar ajustes para la convención 30/360
    if d1 == 31:
        d1 = 30
    if d2 == 31:
        d2 = 30
        
    # Calcular la diferencia de días usando la fórmula 30/360
    dias_diferencia = ((y2 - y1) * 360) + ((m2 - m1) * 30) + (d2 - d1)

    # Sumar 1 para que el cálculo sea inclusivo (contar ambos extremos)
    return dias_diferencia + 1

# Mantener compatibilidad con código que pueda usar calcular_dias_360
calcular_dias_360 = calcular_dias_liquidacion
