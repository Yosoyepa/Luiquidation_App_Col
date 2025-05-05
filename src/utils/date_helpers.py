"""
Utilidades para el manejo de fechas en la aplicación.
"""
import datetime
from typing import Dict, Optional, Tuple
from src.core.constants import DIAS_ANIO_COMERCIAL, DIAS_MES_COMERCIAL

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
    dias_diferencia = ((y2 - y1) * DIAS_ANIO_COMERCIAL) + ((m2 - m1) * DIAS_MES_COMERCIAL) + (d2 - d1)

    # Sumar 1 para que el cálculo sea inclusivo (contar ambos extremos)
    return dias_diferencia + 1

# Mantener compatibilidad con código que pueda usar calcular_dias_360
calcular_dias_360 = calcular_dias_liquidacion

def obtener_fecha_inicio_semestre(anio: int, semestre: int) -> datetime.date:
    """
    Obtiene la fecha de inicio de un semestre específico.
    
    Args:
        anio: Año del semestre
        semestre: Número de semestre (1 o 2)
        
    Returns:
        Fecha de inicio del semestre
        
    Raises:
        ValueError: Si el semestre no es 1 o 2
    """
    if semestre not in [1, 2]:
        raise ValueError("El semestre debe ser 1 o 2")
    
    if semestre == 1:
        return datetime.date(anio, 1, 1)
    else:
        return datetime.date(anio, 7, 1)

def obtener_fecha_fin_semestre(anio: int, semestre: int) -> datetime.date:
    """
    Obtiene la fecha de fin de un semestre específico.
    
    Args:
        anio: Año del semestre
        semestre: Número de semestre (1 o 2)
        
    Returns:
        Fecha de fin del semestre
        
    Raises:
        ValueError: Si el semestre no es 1 o 2
    """
    if semestre not in [1, 2]:
        raise ValueError("El semestre debe ser 1 o 2")
    
    if semestre == 1:
        return datetime.date(anio, 6, 30)
    else:
        return datetime.date(anio, 12, 31)

def calcular_dias_por_semestre(fecha_inicio: datetime.date, fecha_fin: datetime.date) -> Dict[int, int]:
    """
    Calcula los días trabajados (30/360) correspondientes a cada semestre
    dentro del periodo dado.
    
    Esta función determina cuántos días del periodo caen en cada uno de los
    semestres del año de referencia (fecha_fin.year). Es especialmente útil
    para cálculos como la prima de servicios que se liquidan semestralmente.

    Args:
        fecha_inicio: Fecha de inicio del periodo
        fecha_fin: Fecha de fin del periodo
        
    Returns:
        Un diccionario {1: dias_sem1, 2: dias_sem2} con los días correspondientes
        a cada semestre.
        
    Raises:
        ValueError: Si fecha_fin es anterior a fecha_inicio
    """
    if fecha_fin < fecha_inicio:
        raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")

    dias_sem1 = 0
    dias_sem2 = 0

    # Definir el año de referencia (normalmente el de la fecha fin para liquidaciones)
    anio_referencia = fecha_fin.year
    
    # Obtener límites de los semestres del año de referencia
    inicio_sem1 = obtener_fecha_inicio_semestre(anio_referencia, 1)
    fin_sem1 = obtener_fecha_fin_semestre(anio_referencia, 1)
    inicio_sem2 = obtener_fecha_inicio_semestre(anio_referencia, 2)
    fin_sem2 = obtener_fecha_fin_semestre(anio_referencia, 2)

    # Calcular días en Semestre 1 (si hay intersección)
    if not (fecha_fin < inicio_sem1 or fecha_inicio > fin_sem1):
        # Determinar el periodo efectivo de intersección con el semestre 1
        inicio_efectivo_s1 = max(fecha_inicio, inicio_sem1)
        fin_efectivo_s1 = min(fecha_fin, fin_sem1)
        
        # Calcular días en el primer semestre
        dias_sem1 = calcular_dias_liquidacion(inicio_efectivo_s1, fin_efectivo_s1)

    # Calcular días en Semestre 2 (si hay intersección)
    if not (fecha_fin < inicio_sem2 or fecha_inicio > fin_sem2):
        # Determinar el periodo efectivo de intersección con el semestre 2
        inicio_efectivo_s2 = max(fecha_inicio, inicio_sem2)
        fin_efectivo_s2 = min(fecha_fin, fin_sem2)
        
        # Calcular días en el segundo semestre
        dias_sem2 = calcular_dias_liquidacion(inicio_efectivo_s2, fin_efectivo_s2)

    # Verificación de consistencia
    dias_totales = calcular_dias_liquidacion(fecha_inicio, fecha_fin)
    if dias_sem1 + dias_sem2 > dias_totales + 1:  # +1 por posible doble conteo
        # Ajustar si hay inconsistencia (raro, pero posible en casos límite)
        print(f"Advertencia: Ajuste necesario en cálculo de días por semestre. Total: {dias_totales}, Sum: {dias_sem1 + dias_sem2}")
        # En este caso simple, asumimos que la distribución proporcional es suficiente
        factor = dias_totales / (dias_sem1 + dias_sem2)
        dias_sem1 = int(dias_sem1 * factor)
        dias_sem2 = dias_totales - dias_sem1

    return {1: dias_sem1, 2: dias_sem2}

# Para compatibilidad con código existente
_calcular_dias_por_semestre = calcular_dias_por_semestre
