import sympy as sp

from tools.logger import console_log
from utilities.enumerations import LogTypes

x = sp.Symbol('x')


def derivar_funcion(funcion, orden=1):
    try:
        return sp.diff(funcion, (x, orden))
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def evaluar_funcion(funcion, punto):
    try:
        return funcion.subs(x, punto).evalf()
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_error_relativo(ultimo_resultado, resultado_anterior):
    try:
        return abs(ultimo_resultado - resultado_anterior)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_epsilon(funcion, puntos_criticos):
    try:  #todo factorizar
        mayor = 0
        resultado = 0
        if type(puntos_criticos) is not None:
            iteracion = -1
            for punto in puntos_criticos:
                iteracion += 1
                imagen = evaluar_funcion(funcion, punto)
                if mayor < imagen:
                    mayor = imagen
                    resultado = punto
            return resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_raices(funcion, inicio_intervalo, final_intervalo):
    try:
        return sp.solveset(funcion, x, domain=sp.Interval(inicio_intervalo, final_intervalo))
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_punto_medio(inicio_intervalo, final_intervalo):
    try:
        return (inicio_intervalo + final_intervalo) / 2
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def es_par(numero):
    try:
        return numero % 2 == 0
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def es_multiplo(numero, factor):
    try:
        return numero % factor == 0
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))
