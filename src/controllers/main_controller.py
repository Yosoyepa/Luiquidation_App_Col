# src/controllers/main_controller.py
import datetime
from src.core import calculator  # Importa el módulo de cálculo
from src.ui.main_window import MainWindow # Podría necesitar referencia a la ventana o frames

class MainController:
    """
    Controlador principal que maneja la interacción entre la UI y la lógica de negocio.
    """
    def __init__(self, view: MainWindow):
        """
        Inicializa el controlador.

        Args:
            view: La instancia de la ventana principal (MainWindow).
        """
        self.view = view
        self.input_frame = view.get_input_frame()
        self.results_frame = view.get_results_frame()

        # Conectar el botón de la vista a la acción del controlador
        self.input_frame.set_button_command(self._on_calculate_dias_click)

    def _on_calculate_dias_click(self):
        """
        Manejador para el evento de clic en el botón 'Calcular Días'.
        Obtiene las fechas de la UI, llama a la función de cálculo y
        actualiza la UI con el resultado.
        """
        try:
            fecha_inicio = self.input_frame.get_fecha_inicio()
            fecha_fin = self.input_frame.get_fecha_fin()

            # Llamar a la función de cálculo del módulo core
            dias_calculados = calculator.calcular_dias_liquidacion(fecha_inicio, fecha_fin)

            # Actualizar el frame de resultados
            self.results_frame.update_result(f"Días calculados: {dias_calculados}")

        except ValueError as e:
            # Manejar error si fecha_fin < fecha_inicio
            self.results_frame.update_result(f"Error: {e}")
        except Exception as e:
            # Capturar otros posibles errores inesperados
            self.results_frame.update_result(f"Error inesperado: {e}")
            print(f"Error inesperado en cálculo: {e}") # Log adicional a consola