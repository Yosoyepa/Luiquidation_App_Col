# -*- coding: utf-8 -*-

"""
config/settings.py

Archivo de configuración central para la aplicación de liquidaciones laborales.
Contiene valores constantes y datos históricos que pueden ser necesarios
para los cálculos según la normativa colombiana.

IMPORTANTE: Los valores de Salario Mínimo y Auxilio de Transporte se definen
anualmente. Asegúrate de mantener esta información actualizada para garantizar
la precisión de los cálculos. La fuente oficial suele ser el Ministerio
del Trabajo de Colombia o los decretos presidenciales correspondientes.
"""

from typing import Dict, Final
import datetime

# --- Año Actual (Para fácil acceso a los valores vigentes) ---
# Obtenemos el año actual basado en la fecha del sistema al momento de correr el script.
# Si la aplicación corre en diferentes momentos, esto dará el año en curso.
# Para asegurar el año de cálculo correcto, la lógica de la app debería
# basarse en las fechas de inicio/fin del contrato, no sólo en este valor.
CURRENT_YEAR: Final[int] = datetime.datetime.now().year 

# --- Datos Históricos del Salario Mínimo Mensual Legal Vigente (SMMLV) ---
# Fuente: Decretos anuales del Gobierno de Colombia.
# Valores en pesos colombianos (COP), sin puntos ni comas.
SALARIOS_MINIMOS_HISTORICOS: Final[Dict[int, int]] = {
    2020: 877803,
    2021: 908526,
    2022: 1000000,
    2023: 1160000,
    2024: 1300000,
    # Valor 2025: Decretado a finales de 2024. 
    # Usando el valor correspondiente al año actual (2025) según la fecha del sistema.
    2025: 1423500, # Ejemplo basado en la fecha actual del sistema (02 May 2025) - ¡VERIFICAR VALOR OFICIAL DECRETADO! 
}

# --- Datos Históricos del Auxilio de Transporte ---
# Fuente: Decretos anuales del Gobierno de Colombia.
# Valores en pesos colombianos (COP), sin puntos ni comas.
# Nota: Aplica para trabajadores que devenguen hasta 2 SMMLV.
AUXILIOS_TRANSPORTE_HISTORICOS: Final[Dict[int, int]] = {
    2020: 102854,
    2021: 106454,
    2022: 117172,
    2023: 140606,
    2024: 162000,
    # Valor 2025: Decretado a finales de 2024.
    # Usando el valor correspondiente al año actual (2025) según la fecha del sistema.
    2025: 200000, # Ejemplo basado en la fecha actual del sistema (02 May 2025) - ¡VERIFICAR VALOR OFICIAL DECRETADO!
}

# --- Valores Vigentes (para el año actual detectado) ---
# Se obtienen directamente de los diccionarios históricos para consistencia.
# La lógica de cálculo debería usar el año relevante del periodo a liquidar.
try:
    SALARIO_MINIMO_VIGENTE: Final[int] = SALARIOS_MINIMOS_HISTORICOS.get(CURRENT_YEAR, 0)
    AUXILIO_TRANSPORTE_VIGENTE: Final[int] = AUXILIOS_TRANSPORTE_HISTORICOS.get(CURRENT_YEAR, 0)
except KeyError:
    # Manejo por si el año actual no está en el diccionario (improbable si se actualiza)
    print(f"ADVERTENCIA: No se encontraron datos para el año {CURRENT_YEAR} en config/settings.py. Usando $0.")
    SALARIO_MINIMO_VIGENTE = 0
    AUXILIO_TRANSPORTE_VIGENTE = 0
    
# --- Otros Parámetros Configurables (Ejemplos) ---

# Porcentaje de Intereses sobre Cesantías (Fijo por ley)
PORCENTAJE_INTERESES_CESANTIAS: Final[float] = 0.12 # Equivale al 12% anual

# Número máximo de SMMLV para tener derecho al Auxilio de Transporte
MAX_SMMLV_PARA_AUXILIO_TRANSPORTE: Final[int] = 2

# Podrías añadir aquí otros valores como UVT si fueran necesarios para cálculos específicos.

# Porcentaje de Intereses sobre Cesantías (Fijo por ley)
PORCENTAJE_INTERESES_CESANTIAS: Final[float] = 0.12 # Equivale al 12% anual

# --- Funciones de utilidad para acceder a los datos ---

def obtener_smmlv(anio: int) -> int:
    """
    Obtiene el Salario Mínimo Mensual Legal Vigente (SMMLV) para un año específico.
    Retorna 0 si el año no se encuentra en el histórico.
    """
    return SALARIOS_MINIMOS_HISTORICOS.get(anio, 0)

def obtener_auxilio_transporte(anio: int) -> int:
    """
    Obtiene el Auxilio de Transporte para un año específico.
    Retorna 0 si el año no se encuentra en el histórico.
    """
    return AUXILIOS_TRANSPORTE_HISTORICOS.get(anio, 0)

# --- Verificación rápida al cargar el módulo ---
if __name__ == "__main__":
    print(f"Configuración cargada para el año actual ({CURRENT_YEAR}):")
    print(f"  - SMMLV {CURRENT_YEAR}: ${SALARIO_MINIMO_VIGENTE:,}")
    print(f"  - Aux. Transporte {CURRENT_YEAR}: ${AUXILIO_TRANSPORTE_VIGENTE:,}")
    
    # Ejemplo de uso de las funciones
    year_consulta = 2023
    print(f"\nConsulta para el año {year_consulta}:")
    smmlv_2023 = obtener_smmlv(year_consulta)
    aux_2023 = obtener_auxilio_transporte(year_consulta)
    print(f"  - SMMLV {year_consulta}: ${smmlv_2023:,}")
    print(f"  - Aux. Transporte {year_consulta}: ${aux_2023:,}")