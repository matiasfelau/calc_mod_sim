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


def ejecutar_procedimiento_runge_kutta_4(funcion, y_inicial, inicio_intervalo, final_intervalo, paso):
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
            primer_pendiente = evaluar_funcion_dos_variables(funcion, x_actual, y_actual)
            x_segunda_pendiente = x_actual + (paso / 2)
            y_segunda_pendiente = y_actual + (primer_pendiente / 2)
            segunda_pendiente = evaluar_funcion_dos_variables(funcion, x_segunda_pendiente, y_segunda_pendiente)
            x_tercer_pendiente = x_segunda_pendiente
            y_tercer_pendiente = y_actual + (segunda_pendiente / 2)
            tercer_pendiente = evaluar_funcion_dos_variables(funcion, x_tercer_pendiente, y_tercer_pendiente)
            x_cuarta_pendiente = x_actual + paso
            y_cuarta_pendiente = y_actual + tercer_pendiente
            cuarta_pendiente = evaluar_funcion_dos_variables(funcion, x_cuarta_pendiente, y_cuarta_pendiente)
            y_siguiente = y_actual + (paso / 6) * (primer_pendiente + 2 * segunda_pendiente + 2 * tercer_pendiente + cuarta_pendiente)
        print_procedure_result_table(resultado, ['n', 'xn', 'yn'])
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar_procedimiento_runge_kutta_4(fx, y0, inicio, final, h)
