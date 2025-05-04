# src/controllers/main_controller.py
import datetime
import locale # Para formatear moneda
from src.core import calculator
from src.ui.main_window import MainWindow
# Importar los tipos de frame específicos es útil para type hinting
from src.ui.frames.main_menu_frame import MainMenuFrame
from src.ui.frames.days_calculator_frame import DaysCalculatorFrame
from src.ui.frames.cesantias_frame import CesantiasFrame

# Configurar locale para formato de moneda COP (opcional pero recomendado)
try:
    # Intenta configurar para Colombia, puede fallar si el locale no está en el sistema
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
except locale.Error:
    try:
        # Intenta con un locale genérico en español
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except locale.Error:
        # Fallback si no se puede configurar español
        print("Advertencia: No se pudo configurar el locale a español. El formato de moneda puede no ser correcto.")
        # locale.setlocale(locale.LC_ALL, '') # Usa el locale por defecto del sistema


class MainController:
    """
    Controlador principal que maneja navegación y lógica de UI.
    """
    def __init__(self, view: MainWindow):
        self.view = view
        self.current_mode = "Laboral" # Modo inicial

        # Obtener referencias a los frames gestionados por la vista
        self.main_menu_frame: MainMenuFrame = view.get_frame("MainMenuFrame")
        self.days_calc_frame: DaysCalculatorFrame = view.get_frame("DaysCalculatorFrame")
        self.cesantias_frame: CesantiasFrame = view.get_frame("CesantiasFrame")

        # Conectar comandos de navegación del menú principal
        self.main_menu_frame.set_calc_dias_command(self.show_days_calculator)
        self.main_menu_frame.set_cesantias_command(self.show_cesantias_calculator)
        # Conectar botones de modo (si se necesita más lógica que la visual)
        # self.main_menu_frame.button_laboral.configure(command=lambda: self.change_mode("Laboral"))

        # Conectar comandos de acción y 'volver' de los frames específicos
        # Para Days Calculator
        days_input_frame = self.days_calc_frame.get_input_frame()
        days_input_frame.set_button_command(self._on_calculate_dias_click)
        self.days_calc_frame.set_back_command(self.show_main_menu)

        # Para Cesantías Calculator
        self.cesantias_frame.set_calculate_command(self._on_calculate_cesantias_click)
        self.cesantias_frame.set_back_command(self.show_main_menu)

    # --- Métodos de Navegación ---
    def show_main_menu(self):
        self.view.show_frame("MainMenuFrame")

    def show_days_calculator(self):
        self.view.show_frame("DaysCalculatorFrame")

    def show_cesantias_calculator(self):
         # Limpiar campos previos antes de mostrar (opcional)
        self.cesantias_frame.update_result("Cesantías: -")
        # self.cesantias_frame.entry_salario.delete(0, "end")
        self.view.show_frame("CesantiasFrame")

    # --- Métodos de Callback para Cálculos ---
    def _on_calculate_dias_click(self):
        """Calcula los días 30/360 desde DaysCalculatorFrame."""
        days_input_frame = self.days_calc_frame.get_input_frame()
        days_results_frame = self.days_calc_frame.get_results_frame()
        try:
            fecha_inicio = days_input_frame.get_fecha_inicio()
            fecha_fin = days_input_frame.get_fecha_fin()
            dias_calculados = calculator.calcular_dias_liquidacion(fecha_inicio, fecha_fin)
            days_results_frame.update_result(f"Días calculados (30/360): {dias_calculados}")
        except ValueError as e:
            days_results_frame.update_result(f"Error: {e}")
        except Exception as e:
            days_results_frame.update_result(f"Error inesperado: {e}")
            print(f"Error inesperado en cálculo días: {e}")

    def _on_calculate_cesantias_click(self):
        """Calcula las cesantías desde CesantiasFrame."""
        try:
            inputs = self.cesantias_frame.get_inputs()
            # Usar el año de la fecha fin como referencia para SMMLV/Auxilio
            anio = inputs["fecha_fin"].year

            cesantias_valor = calculator.calcular_cesantias(
                salario_mensual=inputs["salario_mensual"],
                fecha_inicio=inputs["fecha_inicio"],
                fecha_fin=inputs["fecha_fin"],
                anio_liquidacion=anio # Pasar el año relevante
            )
            # Formatear como moneda COP
            resultado_formateado = locale.currency(cesantias_valor, grouping=True, symbol=True)
            self.cesantias_frame.update_result(f"Cesantías Calculadas: {resultado_formateado}")

        except ValueError as e:
            self.cesantias_frame.update_result(f"Error: {e}")
        except Exception as e:
            self.cesantias_frame.update_result(f"Error inesperado: {e}")
            print(f"Error inesperado en cálculo cesantías: {e}")

    # --- Otros métodos (ej: cambiar modo) ---
    # def change_mode(self, mode):
    #     self.current_mode = mode
    #     self.main_menu_frame.select_mode(mode)
    #     # Actualizar UI o lógica basada en el modo si es necesario
    #     print(f"Modo cambiado a: {self.current_mode}")