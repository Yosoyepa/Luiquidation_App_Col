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
    "VACACIONES": "Vacaciones",
    "INDEM_DESPIDO": "Indemnización por Despido"
}