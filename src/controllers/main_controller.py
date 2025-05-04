# src/controllers/main_controller.py
import datetime
import locale # Para formatear moneda
import src.ui.theme as theme # Importar theme para usar colores en mensajes si es necesario
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

        # --- Conectar comandos de navegación del MainMenuFrame ---
        # Usar el método 'set_card_command' del MainMenuFrame actualizado,
        # pasando la clave de la tarjeta y el método del controlador a llamar.
        self.main_menu_frame.set_card_command("CalcDias", self.show_days_calculator)
        self.main_menu_frame.set_card_command("Cesantias", self.show_cesantias_calculator)
        # Conectar otras tarjetas aquí cuando implementes sus vistas y lógica:
        # self.main_menu_frame.set_card_command("Vacaciones", self.show_vacaciones_calculator)
        # self.main_menu_frame.set_card_command("Prima", self.show_prima_calculator)
        # ... y así sucesivamente para las demás tarjetas ...

        # Conectar botones de modo si se necesita lógica adicional al seleccionar modo
        # (La lógica visual ya está en MainMenuFrame.select_mode)
        # for mode, button in self.main_menu_frame.buttons_sidebar.items():
        #     if button.cget("state") == "normal": # Solo conectar si no está deshabilitado
        #         button.configure(command=lambda m=mode: self.change_mode(m))

        # --- Conectar comandos de acción y 'volver' de los frames específicos ---

        # Para Days Calculator Frame:
        # Asume que DaysCalculatorFrame tiene un método get_input_frame()
        # y que InputFrame todavía tiene el botón 'Calcular Días' y set_button_command()
        try:
            days_input_frame = self.days_calc_frame.get_input_frame()
            # Conectar el botón 'Calcular' dentro de InputFrame
            days_input_frame.set_button_command(self._on_calculate_dias_click)
        except AttributeError as e:
             print(f"Advertencia: No se pudo conectar el botón de cálculo en DaysCalculatorFrame/InputFrame. ¿Estructura cambiada? Error: {e}")
        # Conectar el botón 'Volver' de DaysCalculatorFrame
        self.days_calc_frame.set_back_command(self.show_main_menu)

        # Para Cesantías Calculator Frame:
        # Conectar el botón 'Calcular Cesantías'
        self.cesantias_frame.set_calculate_command(self._on_calculate_cesantias_click)
        # Conectar el botón 'Volver'
        self.cesantias_frame.set_back_command(self.show_main_menu)

    # --- Métodos de Navegación (sin cambios respecto a tu versión) ---
    def show_main_menu(self):
        """Muestra el frame del menú principal."""
        self.view.show_frame("MainMenuFrame")

    def show_days_calculator(self):
        """Muestra el frame de la calculadora de días."""
        # Podrías limpiar el resultado anterior si lo deseas
        # result_frame = self.days_calc_frame.get_results_frame()
        # result_frame.update_result("Días calculados (30/360): -")
        self.view.show_frame("DaysCalculatorFrame")

    def show_cesantias_calculator(self):
        """Muestra el frame de la calculadora de cesantías."""
        # Limpiar campos y resultado antes de mostrar
        self.cesantias_frame.update_result("Cesantías: -")
        # Podrías también limpiar los campos de entrada aquí si quieres:
        # self.cesantias_frame.entry_salario.delete(0, "end")
        # self.cesantias_frame.date_entry_inicio.set_date(datetime.date.today()) # Resetear fechas?
        # self.cesantias_frame.date_entry_fin.set_date(datetime.date.today())
        self.view.show_frame("CesantiasFrame")

    # --- Métodos de Callback para Cálculos (sin cambios respecto a tu versión) ---
    def _on_calculate_dias_click(self):
        """Calcula los días 30/360 desde DaysCalculatorFrame."""
        # Acceder a los sub-frames a través del frame contenedor
        days_input_frame = self.days_calc_frame.get_input_frame()
        days_results_frame = self.days_calc_frame.get_results_frame()
        try:
            fecha_inicio = days_input_frame.get_fecha_inicio()
            fecha_fin = days_input_frame.get_fecha_fin()
            dias_calculados = calculator.calcular_dias_liquidacion(fecha_inicio, fecha_fin)
            # Actualizar el frame de resultados específico
            days_results_frame.update_result(f"Días calculados (30/360): {dias_calculados}")
        except ValueError as e:
            days_results_frame.update_result(f"Error: {e}")
            # Podrías usar theme.COLOR_ERROR_TEXT si la etiqueta lo soporta
            # days_results_frame.result_label.configure(text_color=theme.COLOR_ERROR_TEXT)
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
            # Formatear como moneda COP usando el locale configurado
            resultado_formateado = locale.currency(cesantias_valor, grouping=True, symbol='COP ') # Añadir 'COP ' como símbolo
            self.cesantias_frame.update_result(f"Cesantías Calculadas: {resultado_formateado}")
            # Podrías cambiar el color del texto a éxito
            # self.cesantias_frame.result_label.configure(text_color=theme.COLOR_SUCCESS_TEXT)

        except ValueError as e:
            self.cesantias_frame.update_result(f"Error: {e}")
            # self.cesantias_frame.result_label.configure(text_color=theme.COLOR_ERROR_TEXT)
        except Exception as e:
            self.cesantias_frame.update_result(f"Error inesperado: {e}")
            # self.cesantias_frame.result_label.configure(text_color=theme.COLOR_ERROR_TEXT)
            print(f"Error inesperado en cálculo cesantías: {e}")

    # --- Otros métodos (ej: cambiar modo - sin cambios respecto a tu versión) ---
    # def change_mode(self, mode):
    #     """ Cambia el modo de cálculo y actualiza la UI si es necesario. """
    #     if self.current_mode != mode:
    #         self.current_mode = mode
    #         # Llama al método del frame para actualizar visualmente el botón seleccionado
    #         self.main_menu_frame.select_mode(mode)
    #         # Podrías añadir lógica aquí para:
    #         # - Habilitar/deshabilitar tarjetas específicas del modo
    #         # - Cambiar títulos o textos en la UI
    #         print(f"Modo de cálculo cambiado a: {self.current_mode}")