import sympy as sp

from herramientas.logger import console_log
from utiles.enumerations import LogTypes

x = sp.Symbol('x')

def derivar_funcion(funcion):
    console_log(LogTypes.STATUS, 'DERIVANDO')
    return sp.diff(funcion, x)

def evaluar_funcion(funcion, punto_evaluado):
    return funcion.subs(x, punto_evaluado).evalf(9)

def calcular_error(resultado_actual, resultado_anterior):
    return round(abs(resultado_actual - resultado_anterior), 9)
