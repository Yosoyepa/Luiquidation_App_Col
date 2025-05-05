# -*- coding: utf-8 -*-

"""
src/core/calculator.py

Este módulo contiene la lógica central para los cálculos de liquidación laboral
basados en el Código Sustantivo del Trabajo de Colombia y prácticas comunes.
"""

import datetime
from typing import Optional 
from config import settings # Importar la configuración
# Nota: Añadir otras importaciones necesarias a medida que se añaden más funciones
# Por ejemplo: from config import settings

# ==============================================================================
# Funciones de Cálculo de Días
# ==============================================================================

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

    # --- Aplicar ajustes para la convención 30/360 ---
    if d1 == 31:
        d1 = 30
    if d2 == 31:
        d2 = 30
        
    # --- Calcular la diferencia de días usando la fórmula 30/360 ---
    dias_diferencia = ((y2 - y1) * 360) + ((m2 - m1) * 30) + (d2 - d1)

    # --- Sumar 1 para que el cálculo sea inclusivo (contar ambos extremos) ---
    dias_totales = dias_diferencia + 1

    return dias_totales


# ==============================================================================
# Funciones de Cálculo de Prestaciones
# ==============================================================================

def calcular_cesantias(
    salario_mensual: float,
    fecha_inicio: datetime.date,
    fecha_fin: datetime.date,
    anio_liquidacion: Optional[int] = None # Año para buscar SMMLV/Auxilio
) -> float:
    """
    Calcula el valor de las cesantías para un periodo determinado.

    Args:
        salario_mensual: Salario mensual base del empleado.
        fecha_inicio: Fecha de inicio del periodo de cálculo.
        fecha_fin: Fecha de fin del periodo de cálculo.
        anio_liquidacion: El año para el cual se consultan el SMMLV y Aux. Transporte.
                          Si es None, se usará el año de la fecha_fin.

    Returns:
        El valor calculado de las cesantías para el periodo.

    Raises:
        ValueError: Si las fechas son inválidas o falta configuración para el año.
    """
    if anio_liquidacion is None:
        anio_liquidacion = fecha_fin.year

    # Obtener SMMLV y Auxilio de Transporte del año correspondiente
    smmlv_anio = settings.obtener_smmlv(anio_liquidacion)
    auxilio_transporte_anio = settings.obtener_auxilio_transporte(anio_liquidacion)

    if smmlv_anio <= 0 or auxilio_transporte_anio <= 0:
        raise ValueError(f"No se encontró configuración de SMMLV/Aux. Transporte para el año {anio_liquidacion}")

    # Determinar si aplica el auxilio de transporte
    aplica_auxilio = salario_mensual <= (settings.MAX_SMMLV_PARA_AUXILIO_TRANSPORTE * smmlv_anio)

    # Calcular el salario base para la liquidación (incluye auxilio si aplica)
    salario_base_liquidacion = salario_mensual
    if aplica_auxilio:
        salario_base_liquidacion += auxilio_transporte_anio

    # Calcular los días trabajados en el periodo usando la función existente
    dias_trabajados = calcular_dias_liquidacion(fecha_inicio, fecha_fin)

    # Calcular las cesantías: (Salario Base * Días Trabajados) / 360
    # Asegurarse de usar float para la división
    cesantias = (float(salario_base_liquidacion) * dias_trabajados) / 360.0

    # Considerar redondeo si es necesario (ej. al peso más cercano)
    # return round(cesantias)
    return cesantias


def calcular_intereses_cesantias(
    valor_cesantias: float,
    fecha_inicio: datetime.date,
    fecha_fin: datetime.date
) -> float:
    """
    Calcula los intereses sobre las cesantías para un periodo determinado.

    Formula: (Valor Cesantías * Días Trabajados * 0.12) / 360

    Args:
        valor_cesantias: El monto de las cesantías calculado para el periodo.
        fecha_inicio: Fecha de inicio del periodo de cálculo (para calcular días).
        fecha_fin: Fecha de fin del periodo de cálculo (para calcular días).

    Returns:
        El valor calculado de los intereses sobre cesantías.

    Raises:
        ValueError: Si las fechas son inválidas.
    """
    # Calcular los días trabajados para el periodo
    # Nota: Se podría pasar dias_trabajados como argumento si ya se calculó externamente
    #       para evitar recalcularlo. Por ahora, lo calculamos aquí.
    try:
        dias_trabajados = calcular_dias_liquidacion(fecha_inicio, fecha_fin)
    except ValueError as e:
        # Re-lanzar el error si las fechas son inválidas
        raise ValueError(f"Error al calcular días para intereses: {e}")

    if dias_trabajados < 0: # Validación extra
        raise ValueError("Los días trabajados no pueden ser negativos.")

    # Obtener la tasa de interés desde la configuración
    tasa_interes = settings.PORCENTAJE_INTERESES_CESANTIAS

    # Calcular los intereses
    intereses = (valor_cesantias * dias_trabajados * tasa_interes) / 360.0

    return intereses


# ... (Resto de funciones: intereses_cesantias, prima, vacaciones, etc. a implementar) ...

# ... (Función Orquestadora calcular_liquidacion_final a implementar) ...



