import sympy as sp
from sympy import Function

from tools.logger import console_log
from utilities.enumerations import LogTypes

x = sp.Symbol('x')
f = Function('f')
y = sp.Symbol('y')


def derivar_funcion(funcion, orden=1):
    """
    derivada de k = 0
    derivada de x = 1
    derivada de x^(n) = nx^(n-1)
    derivada de 1/x = -1/x^(2)
    derivada de sqrt(x) = 1/2sqrt(x)
    derivada de senx = cosx
    derivada de cosx = -sinx
    derivada de tgx = 1/cos^(2)x
    derivada de lnx = 1/x
    derivada de e^(x) = e^(x)
    derivada de a^(x) = a^(x) lna
    derivada de arcsin = 1/sqrt(1-x^(2))
    derivada de arccos = -1/sqrt(1-x^(2))
    derivada de arctan = 1/1+x^(2)
    derivada de e^(mkx) = mke^(mkx)
    """
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


def calcular_integral_definida(funcion, inicio_intervalo, final_intervalo):
    """
    una vaca sin cola vestida de uniforme
    liate para u
    integral de k = kx
    integral de x = x^(n+1)/n+1
    integral de 1/x = lnx
    integral de e^(x) = e^(x)
    integral de a^(x) = a^(x)/lna
    integral de senx = -cosx
    integral de cosx = senx
    integral de 1/cos^(2)x = tgx
    integral de e^(mkx) = me^(mkx)/k
    """
    try:
        return sp.integrate(funcion, (inicio_intervalo, final_intervalo))
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def evaluar_funcion_dos_variables(funcion, primer_variable, segunda_variable):
    try:
        return funcion.subs({x: primer_variable, y: segunda_variable}).evalf()
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))
