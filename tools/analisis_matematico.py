import sympy as sp

from tools.logger import console_log
from utilities.enumerations import LogTypes

from configuration.parameters import precision

from sympy import Float

x = sp.Symbol('x')

def derivar_funcion(funcion):
    try:
        return sp.diff(funcion, x)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def evaluar_funcion(funcion, punto):
    try:
        return funcion.subs(x, punto).evalf(precision)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error(ultimo_resultado, resultado_anterior):
    try:
        return round(abs(ultimo_resultado - resultado_anterior), precision)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_punto_maximo(funcion, intervalo):
    try: #todo factorizar
        primer_derivada = derivar_funcion(funcion)
        puntos_criticos = calcular_raices_intervalo(primer_derivada, intervalo)
        segunda_derivada = derivar_funcion(primer_derivada)
        fue_encontrado = False
        mayor = evaluar_funcion(funcion, puntos_criticos[0])
        resultado = 0
        for punto in puntos_criticos:
            if evaluar_funcion(segunda_derivada, punto) != 0: #todo factorizar
                if mayor < evaluar_funcion(funcion, punto):
                    mayor = evaluar_funcion(funcion, punto)
                    resultado = punto
                    fue_encontrado = True
        if fue_encontrado:
            return resultado
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

def calcular_punto_medio(inicio, final):
    try:
        return round(((inicio + final) / 2), precision)
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