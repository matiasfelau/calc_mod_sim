import sympy as sp

from tools.logger import console_log
from utilities.enumerations import LogTypes

x = sp.Symbol('x')

def derivar_funcion(funcion):
    try:
        return sp.diff(funcion, x)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def evaluar_funcion(funcion, punto):
    try:
        return funcion.subs(x, punto).evalf(9)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_relativo(ultimo_resultado, resultado_anterior):
    try:
        return round(abs(ultimo_resultado - resultado_anterior), 9)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))