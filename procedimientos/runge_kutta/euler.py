import sympy as sp

from tools.analisis_matematico import evaluar_funcion, evaluar_funcion_dos_variables
from tools.logger import console_log
from utilities import vault as v
from configuration import parameters as p
from utilities.enumerations import LogTypes

'''
procedimiento:
1. definir las condiciones iniciales (iteración 0, punto inicial, etc)
iteracion:
2. evaluar la funcion en xn, yn [f(xn, yn)]
3. reemplazar en la formula [yn+1 = yn + h * f(xn, yn)]
'''

def ejecutar_procedimiento_euler(funcion, y_inicial, inicio_intervalo, final_intervalo, paso):
    try:
        y_siguiente = y_inicial
        resultado = []
        for i in range((final_intervalo - inicio_intervalo) / paso):
            x_actual = inicio_intervalo + i * paso
            y_actual = y_siguiente
            resultado.append([i, x_actual, y_actual])
            predictivo = evaluar_funcion_dos_variables(funcion, x_actual, y_actual)
            y_siguiente = y_actual + paso * predictivo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def iterar_euler(funcion, punto_inicial, paso):
    evaluar_funcion_dos_variables(funcion, punto_inicial, paso)