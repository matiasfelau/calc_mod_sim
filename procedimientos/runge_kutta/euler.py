import math

import sympy as sp

from tools.analisis_matematico import evaluar_funcion, evaluar_funcion_dos_variables
from tools.logger import console_log
from tools.printer import print_procedure_result_table
from utilities import vault as v
from configuration import parameters as p
from utilities.enumerations import LogTypes
import sympy as sp

fx = sp.sympify('x*y')
y0 = 1
inicio = 0
final = 2
h = 0.5


def ejecutar_procedimiento_euler(funcion, y_inicial, inicio_intervalo, final_intervalo, paso):
    """
    procedimiento:
    1. definir las condiciones iniciales (iteración 0, punto inicial, etc)
    iteracion:
    2. evaluar la funcion en xn, yn [f(xn, yn)]
    3. reemplazar en la formula [yn+1 = yn + h * f(xn, yn)]
    """
    try:
        y_siguiente = y_inicial
        resultado = []
        for i in range(math.ceil((final_intervalo - inicio_intervalo) / paso)+1):
            x_actual = inicio_intervalo + i * paso
            y_actual = y_siguiente
            resultado.append([i, x_actual, y_actual])
            pendiente = evaluar_funcion_dos_variables(funcion, x_actual, y_actual)
            y_siguiente = y_actual + paso * pendiente
        print_procedure_result_table(resultado, ['n', 'xn', 'yn'])
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar_procedimiento_euler(fx, y0, inicio, final, h)
