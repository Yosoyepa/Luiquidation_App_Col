# src/controllers/main_controller.py
import datetime
import locale
import src.ui.theme as theme
from src.core import calculator
from src.core.constants import CONCEPTOS
from src.core.models import PeriodoLaboral, ResultadoCalculo
from src.ui.main_window import MainWindow
from src.utils.validation import validar_valor_numerico, validar_fechas_periodo
from src.utils.formatting import formatear_moneda, formatear_porcentaje

# Importar los tipos de frame específicos para type hinting
from src.ui.frames.main_menu_frame import MainMenuFrame
from src.ui.frames.days_calculator_frame import DaysCalculatorFrame
from src.ui.frames.cesantias_frame import CesantiasFrame
from src.ui.frames.intereses_cesantias_frame import InteresesCesantiasFrame
from typing import Any, Dict, Optional, Tuple

# --- Configuración de Locale (Importante para formato de moneda) ---
# Intentar configurar para Colombia, manejar posibles errores
try:
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8') # Plan B: Español genérico
    except locale.Error:
        try:
            # Plan C: Locale por defecto del sistema (puede no formatear como COP)
            locale.setlocale(locale.LC_ALL, '')
            print("Advertencia: No se pudo configurar el locale a español. Usando configuración regional del sistema.")
        except locale.Error:
            # Plan D: Si todo falla, al menos no detener la app
             print("ERROR CRÍTICO: No se pudo configurar ningún locale. El formato de moneda fallará.")

# --- Clase Principal del Controlador ---
class MainController:
    """
    Controlador principal que maneja navegación y lógica de UI.
    """
    def __init__(self, view: MainWindow):
        """
        Inicializa el controlador, obtiene referencias a las vistas (frames)
        y conecta los eventos de la UI (botones, tarjetas) a los métodos
        correspondientes del controlador.

        Args:
            view: La instancia de la ventana principal (MainWindow).
        """
        self.view = view
        self.current_mode = "Laboral" # Modo inicial por defecto

        # Obtener referencias a TODOS los frames principales desde la vista
        self.main_menu_frame: Optional[MainMenuFrame] = view.get_frame("MainMenuFrame")
        self.days_calc_frame: Optional[DaysCalculatorFrame] = view.get_frame("DaysCalculatorFrame")
        self.cesantias_frame: Optional[CesantiasFrame] = view.get_frame("CesantiasFrame")
        self.intereses_frame: Optional[InteresesCesantiasFrame] = view.get_frame("InteresesCesantiasFrame")

        # Conectar señales para todos los frames existentes usando métodos helper
        if self.main_menu_frame: self._connect_main_menu_signals()
        else: print("Error: MainMenuFrame no encontrado al inicializar MainController.")

        if self.days_calc_frame: self._connect_days_calculator_signals()
        else: print("Error: DaysCalculatorFrame no encontrado al inicializar MainController.")

        if self.cesantias_frame: self._connect_cesantias_signals()
        else: print("Error: CesantiasFrame no encontrado al inicializar MainController.")

        if self.intereses_frame: self._connect_intereses_signals()
        else: print("Error: InteresesCesantiasFrame no encontrado al inicializar MainController.")

    def _connect_main_menu_signals(self):
        """Conecta los comandos de las tarjetas del menú principal."""
        print("Conectando señales del Menú Principal...")
        # Conectar usando el método 'set_card_command' del MainMenuFrame
        self.main_menu_frame.set_card_command("CalcDias", self.show_days_calculator)
        self.main_menu_frame.set_card_command("Cesantias", self.show_cesantias_calculator)
        self.main_menu_frame.set_card_command("Intereses", self.show_intereses_calculator)
        # Conectar otras tarjetas aquí cuando se implementen...
        # self.main_menu_frame.set_card_command("Prima", self.show_prima_calculator)
        # self.main_menu_frame.set_card_command("Vacaciones", self.show_vacaciones_calculator)

    def _connect_days_calculator_signals(self):
        """Conecta los comandos del frame Calculadora de Días."""
        print("Conectando señales de Calculadora Días...")
        try:
            days_input_frame = self.days_calc_frame.get_input_frame()
            days_input_frame.set_button_command(self._on_calculate_dias_click)
        except AttributeError as e:
             print(f"Advertencia: No se pudo conectar botón cálculo en DaysCalculatorFrame. Error: {e}")
        self.days_calc_frame.set_back_command(self.show_main_menu)

    def _connect_cesantias_signals(self):
        """Conecta los comandos del frame Calculadora de Cesantías."""
        print("Conectando señales de Calculadora Cesantías...")
        self.cesantias_frame.set_calculate_command(self._on_calculate_cesantias_click)
        self.cesantias_frame.set_back_command(self.show_main_menu)

    def _connect_intereses_signals(self):
        """Conecta los comandos del frame Calculadora de Intereses."""
        print("Conectando señales de Calculadora Intereses...")
        self.intereses_frame.set_calculate_command(self._on_calculate_intereses_click)
        self.intereses_frame.set_back_command(self.show_main_menu)

    # --- Métodos de Navegación ---
    def show_main_menu(self):
        """Muestra el frame del menú principal."""
        print("Navegando a: MainMenuFrame")
        self.view.show_frame("MainMenuFrame")

    def show_days_calculator(self):
        """Muestra el frame de la calculadora de días."""
        print("Navegando a: DaysCalculatorFrame")
        if self.days_calc_frame:
             self.view.show_frame("DaysCalculatorFrame")
        else:
             print("Error: DaysCalculatorFrame no disponible.")

    def show_cesantias_calculator(self):
        """Muestra el frame de la calculadora de cesantías e intereses."""
        print("Navegando a: CesantiasFrame")
        if self.cesantias_frame:
            # Limpiar ambos resultados anteriores al mostrar
            self.cesantias_frame.update_results({"cesantias": "Cesantías Calculadas: -", "intereses": "Intereses Cesantías: -"})
            self.view.show_frame("CesantiasFrame")
        else:
             print("Error: CesantiasFrame no disponible.")

    def show_intereses_calculator(self):
        """Muestra el frame de la calculadora de intereses de cesantías (separado)."""
        print("Navegando a: InteresesCesantiasFrame")
        if self.intereses_frame:
            # Limpiar resultado anterior
            self.intereses_frame.update_result("Intereses Calculados: -")
            self.view.show_frame("InteresesCesantiasFrame")
        else:
            print("Error: InteresesCesantiasFrame no disponible.")

    # --- Métodos de Callback para Cálculos ---
    def _on_calculate_dias_click(self):
        """Calcula los días 30/360 desde DaysCalculatorFrame."""
        print("Botón Calcular Días presionado.")
        if not self.days_calc_frame: return

        days_input_frame = self.days_calc_frame.get_input_frame()
        days_results_frame = self.days_calc_frame.get_results_frame()
        try:
            fecha_inicio = days_input_frame.get_fecha_inicio()
            fecha_fin = days_input_frame.get_fecha_fin()
            
            # Validar fechas usando el módulo de validación
            es_valido, mensaje_error = validar_fechas_periodo(fecha_inicio, fecha_fin)
            if not es_valido:
                raise ValueError(mensaje_error)
                
            print(f"Calculando días entre {fecha_inicio} y {fecha_fin}")
            # Usar date_helpers para el cálculo pero mantener compatibilidad con el código existente
            from src.utils.date_helpers import calcular_dias_liquidacion
            dias_calculados = calcular_dias_liquidacion(fecha_inicio, fecha_fin)
            
            print(f"Días calculados: {dias_calculados}")
            days_results_frame.update_result(f"Días calculados (30/360): {dias_calculados}")
        except ValueError as e:
            print(f"Error en cálculo días: {e}")
            days_results_frame.update_result(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado en cálculo días: {e}")
            days_results_frame.update_result(f"Error inesperado: {e}")

    def _on_calculate_cesantias_click(self):
        """
        Calcula las cesantías e intereses desde CesantiasFrame y actualiza la UI.
        """
        print("Botón Calcular Cesantías e Intereses presionado.")
        if not self.cesantias_frame: return

        results_payload: Dict[str, str] = {} # Para enviar a la UI
        try:
            # 1. Obtener y validar entradas de la UI
            inputs = self.cesantias_frame.get_inputs()
            salario_basico = inputs["salario_mensual"]
            fecha_inicio = inputs["fecha_inicio"]
            fecha_fin = inputs["fecha_fin"]
            anio = fecha_fin.year # Año para buscar params
            
            # Validar salario usando el módulo de validación
            es_valido, mensaje_error = validar_valor_numerico(salario_basico, 0, "salario básico")
            if not es_valido:
                raise ValueError(mensaje_error)
                
            # Validar fechas usando el módulo de validación
            es_valido, mensaje_error = validar_fechas_periodo(fecha_inicio, fecha_fin)
            if not es_valido:
                raise ValueError(mensaje_error)
                
            print(f"Inputs Cesantías: Salario Básico={salario_basico}, Inicio={fecha_inicio}, Fin={fecha_fin}, Año Ref={anio}")

            # 2. Crear objeto PeriodoLaboral para encapsular datos de cálculo
            periodo = PeriodoLaboral(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                salario_base=salario_basico,
                incluye_auxilio=False  # Se decidirá en la función de cálculo basado en el valor del salario
            )

            # 3. Calcular Cesantías
            cesantias_valor = calculator.calcular_cesantias(
                salario_mensual=periodo.salario_base,
                fecha_inicio=periodo.fecha_inicio,
                fecha_fin=periodo.fecha_fin,
                anio_liquidacion=anio
            )
            print(f"Cesantías calculadas: {cesantias_valor}")

            # 4. Calcular Intereses sobre Cesantías (depende del valor anterior)
            intereses_valor = calculator.calcular_intereses_cesantias(
                valor_cesantias=cesantias_valor,
                fecha_inicio=periodo.fecha_inicio,
                fecha_fin=periodo.fecha_fin
            )
            print(f"Intereses calculados: {intereses_valor}")

            # 5. Crear ResultadoCalculo objetos para los resultados (opcionalmente)
            resultado_cesantias = ResultadoCalculo(
                concepto=CONCEPTOS["CESANTIAS"],
                valor=cesantias_valor,
                dias_calculados=periodo.dias_laborados,
                fecha_inicio=periodo.fecha_inicio,
                fecha_fin=periodo.fecha_fin
            )
            
            resultado_intereses = ResultadoCalculo(
                concepto=CONCEPTOS["INTERESES"],
                valor=intereses_valor,
                dias_calculados=periodo.dias_laborados,
                fecha_inicio=periodo.fecha_inicio,
                fecha_fin=periodo.fecha_fin
            )

            # 6. Formatear resultados usando el módulo de formateo
            cesantias_formateado = formatear_moneda(resultado_cesantias.valor)
            intereses_formateado = formatear_moneda(resultado_intereses.valor)

            # 7. Preparar payload para la UI
            results_payload["cesantias"] = f"Cesantías Calculadas: {cesantias_formateado}"
            results_payload["intereses"] = f"Intereses Cesantías: {intereses_formateado}"

        except ValueError as e:
            print(f"Error de validación/cálculo Cesantías/Intereses: {e}")
            results_payload["error"] = str(e)
        except Exception as e:
            print(f"Error inesperado en cálculo cesantías/intereses: {e}")
            results_payload["error"] = "Ocurrió un error inesperado."

        # 8. Actualizar la UI
        if hasattr(self.cesantias_frame, 'update_results'):
             self.cesantias_frame.update_results(results_payload)
        else:
             print("Error: CesantiasFrame no tiene el método 'update_results'.")


    def _on_calculate_intereses_click(self):
        """Calcula los intereses sobre cesantías desde InteresesCesantiasFrame."""
        print("Botón Calcular Intereses (separado) presionado.")
        if not self.intereses_frame: return

        try:
            # 1. Obtener y validar entradas de la UI específica de intereses
            inputs = self.intereses_frame.get_inputs()
            valor_cesantias = inputs["valor_cesantias"]
            fecha_inicio = inputs["fecha_inicio"]
            fecha_fin = inputs["fecha_fin"]
            
            # Validación del valor usando el módulo de validación
            es_valido, mensaje_error = validar_valor_numerico(valor_cesantias, 0, "valor de cesantías")
            if not es_valido:
                raise ValueError(mensaje_error)
                
            # Validación de fechas usando el módulo de validación
            es_valido, mensaje_error = validar_fechas_periodo(fecha_inicio, fecha_fin)
            if not es_valido:
                raise ValueError(mensaje_error)
            
            print(f"Inputs Intereses: Valor Cesantías={valor_cesantias}, Inicio={fecha_inicio}, Fin={fecha_fin}")

            # 2. Calcular intereses
            intereses_valor = calculator.calcular_intereses_cesantias(
                valor_cesantias=valor_cesantias,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            print(f"Intereses calculados: {intereses_valor}")

            # 3. Formatear resultado usando el módulo de formateo
            intereses_formateado = formatear_moneda(intereses_valor)
            result_text = f"Intereses Calculados: {intereses_formateado}"
            
            # 4. Actualizar UI
            if hasattr(self.intereses_frame, 'update_result'):
                 self.intereses_frame.update_result(result_text)
            else:
                 print("Error: InteresesCesantiasFrame no tiene el método 'update_result'.")

        except ValueError as e:
             print(f"Error de validación/cálculo Intereses: {e}")
             if hasattr(self.intereses_frame, 'show_error'):
                  self.intereses_frame.show_error(str(e))
             else: # Fallback
                  self.intereses_frame.update_result(f"Error: {e}")
        except Exception as e:
             print(f"Error inesperado en cálculo intereses: {e}")
             if hasattr(self.intereses_frame, 'show_error'):
                  self.intereses_frame.show_error("Ocurrió un error inesperado.")
             else:
                  self.intereses_frame.update_result("Error inesperado.")

    # --- Otros métodos ---
    # def change_mode(self, mode): ...