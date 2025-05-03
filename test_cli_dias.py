# test_cli_dias.py
import datetime
from src.core.calculator import calcular_dias_liquidacion # Importa la función

def run_test():
    print("--- Prueba Rápida de Cálculo de Días (30/360) ---")
    while True:
        try:
            str_inicio = input("Ingrese Fecha Inicio (YYYY-MM-DD): ")
            if not str_inicio: break # Salir si no ingresa nada
            fecha_inicio = datetime.datetime.strptime(str_inicio, "%Y-%m-%d").date()

            str_fin = input("Ingrese Fecha Fin (YYYY-MM-DD):    ")
            if not str_fin: break # Salir si no ingresa nada
            fecha_fin = datetime.datetime.strptime(str_fin, "%Y-%m-%d").date()

            dias = calcular_dias_liquidacion(fecha_inicio, fecha_fin)
            print(f"Resultado -> Días de liquidación: {dias}\n")

        except ValueError as e:
            if "does not match format" in str(e):
                 print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.\n")
            else:
                 print(f"Error: {e}\n") # Ej: Fecha fin anterior a inicio
        except KeyboardInterrupt:
            print("\nSaliendo.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}\n")

if __name__ == "__main__":
    run_test()