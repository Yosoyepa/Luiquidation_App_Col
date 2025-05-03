# -*- coding: utf-8 -*-

"""
src/core/calculator.py

Este módulo contiene la lógica central para los cálculos de liquidación laboral
basados en el Código Sustantivo del Trabajo de Colombia y prácticas comunes.
"""

import datetime
from typing import Optional 
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
# Funciones de Cálculo de Prestaciones (Ejemplos - A desarrollar)
# ==============================================================================

# def calcular_cesantias(salario_base: float, dias_trabajados: int) -> float:
#     """Calcula el valor de las cesantías."""
#     # Importar configuraciones si es necesario (ej: para auxilio transporte)
#     # from config import settings 
#     # Lógica de cálculo según Art. 249 CST y Ley 50/1990
#     # return (salario_base * dias_trabajados) / 360
#     pass

# def calcular_intereses_cesantias(valor_cesantias: float, dias_trabajados: int) -> float:
#     """Calcula los intereses sobre las cesantías."""
#     # from config.settings import PORCENTAJE_INTERESES_CESANTIAS
#     # Lógica de cálculo: ValorCesantias * DiasTrabajados * 0.12 / 360
#     # return (valor_cesantias * dias_trabajados * PORCENTAJE_INTERESES_CESANTIAS) / 360
#     pass

# def calcular_prima_servicios(salario_base: float, dias_trabajados_semestre: int) -> float:
#     """Calcula la prima de servicios para un semestre."""
#     # Lógica de cálculo según Art. 306 CST
#     # return (salario_base * dias_trabajados_semestre) / 360
#     pass

# def calcular_vacaciones_compensadas(salario_base_vacaciones: float, dias_trabajados: int) -> float:
#     """Calcula la compensación en dinero por vacaciones no disfrutadas."""
#     # Lógica de cálculo según Art. 186, 189 CST
#     # return (salario_base_vacaciones * dias_trabajados) / 720
#     pass


# ==============================================================================
# Función Principal de Liquidación (Orquestador - A desarrollar)
# ==============================================================================

# def calcular_liquidacion_final(
#     fecha_inicio_contrato: datetime.date,
#     fecha_fin_contrato: datetime.date,
#     salario_mensual: float,
#     incluye_auxilio_transporte: bool, # Determinado externamente basado en salario y SMMLV
#     # otros parámetros necesarios: tipo_contrato, causa_terminacion, etc.
# ) -> dict:
#     """
#     Orquesta el cálculo completo de la liquidación final del contrato.
#     """
#     dias_totales_liquidacion = calcular_dias_liquidacion(fecha_inicio_contrato, fecha_fin_contrato)
    
#     # Aquí iría la lógica para determinar periodos, bases salariales,
#     # y llamar a las funciones específicas de cálculo (cesantías, prima, etc.)
    
#     resultado = {
#         "dias_liquidacion": dias_totales_liquidacion,
#         "cesantias": 0.0, # calcular_cesantias(...)
#         "intereses_cesantias": 0.0, # calcular_intereses_cesantias(...)
#         "prima_servicios": 0.0, # calcular_prima_servicios(...)
#         "vacaciones_compensadas": 0.0, # calcular_vacaciones_compensadas(...)
#         "indemnizacion": 0.0, # Si aplica
#         "salarios_pendientes": 0.0, # Si aplica
#         "aportes_pendientes": 0.0, # Si aplica (Seguridad Social, Parafiscales)
#         "total_liquidacion": 0.0 
#     }
#     # Calcular el total sumando los componentes
#     # ...
    
#     return resultado