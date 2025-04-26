from procedimientos.runge_kutta.euler import ejecutar_procedimiento_euler
from tools.analisis_matematico import evaluar_funcion_dos_variables
from tools.logger import console_log
from tools.printer import print_procedure_result_table
from utilities.enumerations import LogTypes
import sympy as sp

fx = sp.sympify('fx')
y0 = 0
inicio = 0
final = 1
h = 0.1


def ejecutar_procedimiento_heun(funcion, y_inicial, inicio_intervalo, final_intervalo, paso):
    """
    procedimiento:

    """
    try:
        y_siguiente = y_inicial
        resultado = []
        for i in range((final_intervalo - inicio_intervalo) / paso):
            x_actual = inicio_intervalo + i * paso
            y_actual = y_siguiente
            resultado.append([i, x_actual, y_actual])
            pendiente = evaluar_funcion_dos_variables(funcion, x_actual, y_actual)
            x_siguiente = x_actual + paso
            pendiente_predicha = evaluar_funcion_dos_variables(funcion, x_actual, y_actual)
            y_predicha = y_actual + paso * pendiente_predicha
            predictivo = evaluar_funcion_dos_variables(funcion, x_siguiente, y_predicha)
            y_siguiente = y_actual + (paso / 2) * (pendiente + predictivo)
        print_procedure_result_table(resultado, ['n', 'xn', 'yn'])
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar_procedimiento_heun(fx, y0, inicio, final, h)
