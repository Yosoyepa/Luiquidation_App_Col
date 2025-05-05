# src/controllers/main_controller.py
import datetime
import locale
import src.ui.theme as theme
from src.core import calculator
from src.ui.main_window import MainWindow
# Importar los tipos de frame específicos es útil para type hinting
from src.ui.frames.main_menu_frame import MainMenuFrame
from src.ui.frames.days_calculator_frame import DaysCalculatorFrame
from src.ui.frames.cesantias_frame import CesantiasFrame
# Asegurarse que el import del frame de intereses esté presente
from src.ui.frames.intereses_cesantias_frame import InteresesCesantiasFrame
from typing import Any, Dict

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
        self.main_menu_frame: MainMenuFrame | None = view.get_frame("MainMenuFrame")
        self.days_calc_frame: DaysCalculatorFrame | None = view.get_frame("DaysCalculatorFrame")
        self.cesantias_frame: CesantiasFrame | None = view.get_frame("CesantiasFrame")
        self.intereses_frame: InteresesCesantiasFrame | None = view.get_frame("InteresesCesantiasFrame") # Referencia al frame de intereses

        # Conectar señales para todos los frames existentes usando métodos helper
        if self.main_menu_frame: self._connect_main_menu_signals()
        else: print("Error: MainMenuFrame no encontrado al inicializar MainController.")

        if self.days_calc_frame: self._connect_days_calculator_signals()
        else: print("Error: DaysCalculatorFrame no encontrado al inicializar MainController.")

        if self.cesantias_frame: self._connect_cesantias_signals()
        else: print("Error: CesantiasFrame no encontrado al inicializar MainController.")

        if self.intereses_frame: self._connect_intereses_signals() # Conectar el nuevo frame
        else: print("Error: InteresesCesantiasFrame no encontrado al inicializar MainController.")


    def _connect_main_menu_signals(self):
        """Conecta los comandos de las tarjetas del menú principal."""
        print("Conectando señales del Menú Principal...")
        # Conectar usando el método 'set_card_command' del MainMenuFrame
        self.main_menu_frame.set_card_command("CalcDias", self.show_days_calculator)
        self.main_menu_frame.set_card_command("Cesantias", self.show_cesantias_calculator)
        # Conectar la tarjeta de Intereses (asegurarse que esté habilitada en el frame)
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
            print(f"Calculando días entre {fecha_inicio} y {fecha_fin}")
            dias_calculados = calculator.calcular_dias_liquidacion(fecha_inicio, fecha_fin)
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
            # 1. Obtener entradas de la UI
            inputs = self.cesantias_frame.get_inputs()
            # La clave es "salario_mensual" pero representa el básico sin auxilio
            salario_basico = inputs["salario_mensual"]
            fecha_inicio = inputs["fecha_inicio"]
            fecha_fin = inputs["fecha_fin"]
            anio = fecha_fin.year # Año para buscar params
            print(f"Inputs Cesantías: Salario Básico={salario_basico}, Inicio={fecha_inicio}, Fin={fecha_fin}, Año Ref={anio}")

            if salario_basico <= 0:
                 raise ValueError("El salario básico mensual debe ser mayor a cero.")

            # 2. Calcular Cesantías
            cesantias_valor = calculator.calcular_cesantias(
                salario_mensual=salario_basico, # Pasa el salario básico
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                anio_liquidacion=anio
            )
            print(f"Cesantías calculadas: {cesantias_valor}")

            # 3. Calcular Intereses sobre Cesantías (depende del valor anterior)
            intereses_valor = calculator.calcular_intereses_cesantias(
                valor_cesantias=cesantias_valor,
                fecha_inicio=fecha_inicio, # Se pasan fechas para que calcule días internamente
                fecha_fin=fecha_fin
            )
            print(f"Intereses calculados: {intereses_valor}")

            # 4. Formatear resultados como moneda
            try:
                cesantias_formateado = locale.currency(cesantias_valor, grouping=True, symbol='COP ')
                intereses_formateado = locale.currency(intereses_valor, grouping=True, symbol='COP ')
            except Exception as format_error:
                 print(f"Error formateando moneda con locale: {format_error}. Mostrando números.")
                 cesantias_formateado = f"COP {cesantias_valor:,.2f}"
                 intereses_formateado = f"COP {intereses_valor:,.2f}"

            # 5. Preparar payload para la UI (ambos resultados)
            results_payload["cesantias"] = f"Cesantías Calculadas: {cesantias_formateado}"
            results_payload["intereses"] = f"Intereses Cesantías: {intereses_formateado}"

        except ValueError as e:
            print(f"Error de validación/cálculo Cesantías/Intereses: {e}")
            results_payload["error"] = str(e) # Pasar error para que update_results lo muestre
        except Exception as e:
            print(f"Error inesperado en cálculo cesantías/intereses: {e}")
            results_payload["error"] = "Ocurrió un error inesperado."

        # 6. Actualizar la UI del CesantiasFrame con ambos resultados o error
        # Asegurarse que CesantiasFrame tiene el método update_results
        if hasattr(self.cesantias_frame, 'update_results'):
             self.cesantias_frame.update_results(results_payload)
        else:
             print("Error: CesantiasFrame no tiene el método 'update_results'.")


    def _on_calculate_intereses_click(self):
        """Calcula los intereses sobre cesantías desde InteresesCesantiasFrame."""
        print("Botón Calcular Intereses (separado) presionado.")
        if not self.intereses_frame: return

        try:
            # 1. Obtener entradas de la UI específica de intereses
            inputs = self.intereses_frame.get_inputs()
            valor_cesantias = inputs["valor_cesantias"]
            fecha_inicio = inputs["fecha_inicio"]
            fecha_fin = inputs["fecha_fin"]
            print(f"Inputs Intereses: Valor Cesantías={valor_cesantias}, Inicio={fecha_inicio}, Fin={fecha_fin}")

            if valor_cesantias < 0:
                raise ValueError("El valor de Cesantías no puede ser negativo.")

            # 2. Calcular Intereses
            # Asumiendo que calcular_intereses_cesantias sigue existiendo en calculator.py
            intereses_valor = calculator.calcular_intereses_cesantias(
                valor_cesantias=valor_cesantias,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            print(f"Intereses calculados: {intereses_valor}")

            # 3. Formatear resultado
            try:
                intereses_formateado = locale.currency(intereses_valor, grouping=True, symbol='COP ')
            except Exception as format_error:
                print(f"Error formateando moneda: {format_error}. Mostrando número.")
                intereses_formateado = f"COP {intereses_valor:,.2f}"

            result_text = f"Intereses Calculados: {intereses_formateado}"
            # 4. Actualizar UI del frame de intereses (singular)
            # Asegurarse que InteresesCesantiasFrame tiene update_result
            if hasattr(self.intereses_frame, 'update_result'):
                 self.intereses_frame.update_result(result_text)
            else:
                 print("Error: InteresesCesantiasFrame no tiene el método 'update_result'.")


        except ValueError as e:
             print(f"Error de validación/cálculo Intereses: {e}")
             # Usar show_error del frame de intereses si existe
             if hasattr(self.intereses_frame, 'show_error'):
                  self.intereses_frame.show_error(str(e))
             else: # Fallback si no existe show_error
                  self.intereses_frame.update_result(f"Error: {e}")
        except Exception as e:
             print(f"Error inesperado en cálculo intereses: {e}")
             if hasattr(self.intereses_frame, 'show_error'):
                  self.intereses_frame.show_error("Ocurrió un error inesperado.")
             else:
                  self.intereses_frame.update_result("Error inesperado.")

    # --- Otros métodos ---
    # def change_mode(self, mode): ...