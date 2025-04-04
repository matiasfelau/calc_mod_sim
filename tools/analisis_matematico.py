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

def calcular_error(ultimo_resultado, resultado_anterior):
    try:
        return round(abs(ultimo_resultado - resultado_anterior), 9)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_punto_maximo(funcion, intervalo):
    try:
        primer_derivada = derivar_funcion(funcion)
        puntos_criticos = calcular_raices_intervalo(primer_derivada, intervalo)
        segunda_derivada = derivar_funcion(primer_derivada)
        fue_encontrado = False
        for punto in puntos_criticos:
            if evaluar_funcion(segunda_derivada, punto) < 0:
                fue_encontrado = True
                break
        if fue_encontrado:
            return punto
        else:
            print('No se encontro')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_raices_intervalo(funcion, intervalo):
    try:
        inicio_intervalo = intervalo[0]
        final_intervalo = intervalo[1]
        return sp.solveset(funcion, x, domain=sp.Interval(inicio_intervalo, final_intervalo))
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))