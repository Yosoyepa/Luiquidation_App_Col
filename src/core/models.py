"""
Modelos de datos para la aplicación de liquidación.
"""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, Dict, List, Union

@dataclass
class ParametrosAnio:
    """Representa los parámetros legales para un año específico."""
    anio: int
    salario_minimo: float
    auxilio_transporte: float
    uvt: Optional[float] = None

@dataclass
class PeriodoLaboral:
    """Representa un periodo laboral para cálculos."""
    fecha_inicio: date
    fecha_fin: date
    salario_base: float
    incluye_auxilio: bool = False
    
    @property
    def dias_laborados(self) -> int:
        """Calcula los días laborados en el periodo según convención 30/360."""
        from src.utils.date_helpers import calcular_dias_liquidacion
        return calcular_dias_liquidacion(self.fecha_inicio, self.fecha_fin)

@dataclass
class ResultadoCalculo:
    """Representa el resultado de un cálculo de liquidación."""
    concepto: str
    valor: float
    dias_calculados: int
    fecha_inicio: date
    fecha_fin: date
    detalles: Dict[str, Union[float, str, int]] = field(default_factory=dict)
    
    def formatear_valor(self) -> str:
        """Formatea el valor como moneda."""
        from src.utils.formatting import formatear_moneda
        return formatear_moneda(self.valor)

@dataclass
class ResultadoPrima:
    """Representa el resultado del cálculo de prima de servicios."""
    semestre_1: float
    semestre_2: float
    dias_semestre_1: int
    dias_semestre_2: int
    fecha_inicio: date
    fecha_fin: date
    anio_liquidacion: int
    detalles: Dict[str, Union[float, str, int]] = field(default_factory=dict)
    
    @property
    def total(self) -> float:
        """Calcula el total de la prima para el periodo."""
        return self.semestre_1 + self.semestre_2
    
    def formatear_semestre_1(self) -> str:
        """Formatea el valor del primer semestre como moneda."""
        from src.utils.formatting import formatear_moneda
        return formatear_moneda(self.semestre_1)
    
    def formatear_semestre_2(self) -> str:
        """Formatea el valor del segundo semestre como moneda."""
        from src.utils.formatting import formatear_moneda
        return formatear_moneda(self.semestre_2)
    
    def formatear_total(self) -> str:
        """Formatea el valor total como moneda."""
        from src.utils.formatting import formatear_moneda
        return formatear_moneda(self.total)