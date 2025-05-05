"""
Constantes utilizadas en los cálculos de liquidación.
"""
from typing import Dict, Final

# Porcentajes para cálculos
PORCENTAJE_INTERESES_CESANTIAS: Final[float] = 0.12  # 12% anual
PORCENTAJE_PRIMA: Final[float] = 1.0  # 100% del salario + auxilio / dias periodo * dias trabajados

# Constantes para entitlement
MAX_SMMLV_PARA_AUXILIO_TRANSPORTE: Final[int] = 2

# Factores para cálculos
DIAS_ANIO_COMERCIAL: Final[int] = 360
DIAS_MES_COMERCIAL: Final[int] = 30
DIAS_SEMESTRE_COMERCIAL: Final[int] = 180  # 30 días/mes * 6 meses

# Nomenclatura para tipo de contratos
TIPOS_CONTRATO = {
    "INDEFINIDO": "Término Indefinido",
    "FIJO": "Término Fijo",
    "OBRA_LABOR": "Obra o Labor",
    "SERVICIOS": "Prestación de Servicios"
}

# Conceptos de liquidación
CONCEPTOS = {
    "CESANTIAS": "Cesantías",
    "INTERESES": "Intereses sobre Cesantías",
    "PRIMA": "Prima de Servicios",
    "PRIMA_S1": "Prima de Servicios Semestre 1",
    "PRIMA_S2": "Prima de Servicios Semestre 2",
    "VACACIONES": "Vacaciones",
    "INDEM_DESPIDO": "Indemnización por Despido"
}

# Periodos de liquidación
PERIODOS_LIQUIDACION = {
    "SEMESTRE_1": "Primer Semestre (Enero-Junio)",
    "SEMESTRE_2": "Segundo Semestre (Julio-Diciembre)",
    "ANUAL": "Año Completo"
}