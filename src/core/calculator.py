# -*- coding: utf-8 -*-

"""
src/core/calculator.py

Este módulo contiene la lógica central para los cálculos de liquidación laboral
basados en el Código Sustantivo del Trabajo de Colombia y prácticas comunes.
"""

import datetime
from typing import Optional, Dict, Any
from config import settings
from src.core.constants import (
    PORCENTAJE_INTERESES_CESANTIAS, 
    MAX_SMMLV_PARA_AUXILIO_TRANSPORTE,
    DIAS_ANIO_COMERCIAL
)
from src.utils.date_helpers import calcular_dias_liquidacion
from src.utils.validation import validar_fechas_periodo
from src.core.models import PeriodoLaboral, ResultadoCalculo

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
    # Validar fechas
    es_valido, mensaje_error = validar_fechas_periodo(fecha_inicio, fecha_fin)
    if not es_valido:
        raise ValueError(mensaje_error)
        
    if anio_liquidacion is None:
        anio_liquidacion = fecha_fin.year

    # Obtener SMMLV y Auxilio de Transporte del año correspondiente
    smmlv_anio = settings.obtener_smmlv(anio_liquidacion)
    auxilio_transporte_anio = settings.obtener_auxilio_transporte(anio_liquidacion)

    if smmlv_anio <= 0 or auxilio_transporte_anio <= 0:
        raise ValueError(f"No se encontró configuración de SMMLV/Aux. Transporte para el año {anio_liquidacion}")

    # Determinar si aplica el auxilio de transporte
    aplica_auxilio = salario_mensual <= (MAX_SMMLV_PARA_AUXILIO_TRANSPORTE * smmlv_anio)

    # Calcular el salario base para la liquidación (incluye auxilio si aplica)
    salario_base_liquidacion = salario_mensual
    if aplica_auxilio:
        salario_base_liquidacion += auxilio_transporte_anio

    # Calcular los días trabajados en el periodo
    dias_trabajados = calcular_dias_liquidacion(fecha_inicio, fecha_fin)

    # Calcular las cesantías: (Salario Base * Días Trabajados) / 360
    cesantias = (float(salario_base_liquidacion) * dias_trabajados) / DIAS_ANIO_COMERCIAL

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
    # Validar fechas
    es_valido, mensaje_error = validar_fechas_periodo(fecha_inicio, fecha_fin)
    if not es_valido:
        raise ValueError(mensaje_error)
    
    # Calcular los días trabajados para el periodo
    try:
        dias_trabajados = calcular_dias_liquidacion(fecha_inicio, fecha_fin)
    except ValueError as e:
        # Re-lanzar el error si las fechas son inválidas
        raise ValueError(f"Error al calcular días para intereses: {e}")

    if dias_trabajados < 0: # Validación extra
        raise ValueError("Los días trabajados no pueden ser negativos.")

    # Calcular los intereses usando la constante desde constants.py
    intereses = (valor_cesantias * dias_trabajados * PORCENTAJE_INTERESES_CESANTIAS) / DIAS_ANIO_COMERCIAL

    return intereses


# --- Función de cálculo completo de liquidación ---
def calcular_liquidacion_completa(
    salario_mensual: float,
    fecha_inicio: datetime.date,
    fecha_fin: datetime.date,
    incluir_auxilio: bool = True
) -> Dict[str, ResultadoCalculo]:
    """
    Calcula todos los conceptos de liquidación aplicables para un periodo.
    
    Args:
        salario_mensual: Salario base mensual
        fecha_inicio: Fecha de inicio del periodo
        fecha_fin: Fecha de fin del periodo
        incluir_auxilio: Si debe considerarse el auxilio de transporte según normas
        
    Returns:
        Diccionario con los resultados de cálculo por concepto
    """
    from src.core.constants import CONCEPTOS
    
    # Validar fechas
    es_valido, mensaje_error = validar_fechas_periodo(fecha_inicio, fecha_fin)
    if not es_valido:
        raise ValueError(mensaje_error)
    
    anio_liquidacion = fecha_fin.year
    resultados = {}
    
    # Crear periodo laboral
    periodo = PeriodoLaboral(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        salario_base=salario_mensual,
        incluye_auxilio=incluir_auxilio
    )
    
    # 1. Calcular cesantías
    cesantias_valor = calcular_cesantias(
        salario_mensual=periodo.salario_base,
        fecha_inicio=periodo.fecha_inicio,
        fecha_fin=periodo.fecha_fin,
        anio_liquidacion=anio_liquidacion
    )
    
    resultados["cesantias"] = ResultadoCalculo(
        concepto=CONCEPTOS["CESANTIAS"],
        valor=cesantias_valor,
        dias_calculados=periodo.dias_laborados,
        fecha_inicio=periodo.fecha_inicio,
        fecha_fin=periodo.fecha_fin
    )
    
    # 2. Calcular intereses sobre cesantías
    intereses_valor = calcular_intereses_cesantias(
        valor_cesantias=cesantias_valor,
        fecha_inicio=periodo.fecha_inicio,
        fecha_fin=periodo.fecha_fin
    )
    
    resultados["intereses"] = ResultadoCalculo(
        concepto=CONCEPTOS["INTERESES"],
        valor=intereses_valor,
        dias_calculados=periodo.dias_laborados,
        fecha_inicio=periodo.fecha_inicio,
        fecha_fin=periodo.fecha_fin
    )
    
    # Aquí se pueden añadir más cálculos a medida que se implementen
    # (prima, vacaciones, etc.)
    
    return resultados



