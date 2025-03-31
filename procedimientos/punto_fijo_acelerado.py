import sympy as sp

from tools.analisis_matematico import derivar_funcion, evaluar_funcion, calcular_error_relativo
from tools.logger import console_log
from tools.printer import console_print_table
from procedimientos.punto_fijo import comprobar_contractividad
from utilities.enumerations import LogTypes

gx = sp.sympify("cos(x)") #funcion transformada
x0 = 0.5 #punto inicial
e = 1e-9 #tolerancia del error
nmax = 100 #maximo de iteraciones

def ejecutar(funcion_transformada, punto_inicial, tolerancia_error, maximo_iteraciones):
    try:
        funcion_derivada = derivar_funcion(funcion_transformada)
        console_log(LogTypes.VAR, f'g\'(x) = {funcion_derivada}')
        if comprobar_contractividad(funcion_derivada, punto_inicial):
            resultados = iterar(funcion_transformada, punto_inicial, tolerancia_error, maximo_iteraciones)
            console_print_table(resultados, ['n', 'xₙ', 'xₙ₊₁', 'xₙ₊₂', 'x⁎', 'e'])
        else:
            console_log(LogTypes.WARNING, 'LA FUNCION NO ES CONTRACTIVA')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(funcion_transformada, punto_evaluado, tolerancia_error, maximo_iteraciones):
    try:
        iteracion_actual = -1
        resultados = []
        while True:
            iteracion_actual += 1
            segundo_punto = evaluar_funcion(funcion_transformada, punto_evaluado)
            tercer_punto = evaluar_funcion(funcion_transformada, segundo_punto)
            resultado_iteracion = acelerar(punto_evaluado, segundo_punto, tercer_punto)
            if iteracion_actual == 0:
                resultados.append([iteracion_actual, punto_evaluado, segundo_punto, tercer_punto, resultado_iteracion])
                punto_evaluado = resultado_iteracion
                continue
            error_relativo = calcular_error_relativo(resultado_iteracion, punto_evaluado)
            resultados.append(
                [iteracion_actual, punto_evaluado, segundo_punto, tercer_punto, resultado_iteracion, error_relativo])
            if error_relativo < tolerancia_error or iteracion_actual >= maximo_iteraciones:
                break
            else:
                punto_evaluado = resultado_iteracion
                continue
        return resultados
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def acelerar(primer_punto, segundo_punto, tercer_punto):
    try:
        return primer_punto - (segundo_punto - primer_punto) ** 2 / (tercer_punto - 2 * segundo_punto + primer_punto)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar(gx, x0, e, nmax)
