import sympy as sp

from configuration.parameters import tolerancia, iteraciones
from tools.analisis_matematico import derivar_funcion, evaluar_funcion, calcular_error
from tools.logger import console_log
from tools.printer import console_print_table
from utilities.enumerations import LogTypes

fx = sp.sympify("(x - 1) ** 2") #funcion
x = 0 #punto inicial
e = tolerancia #tolerancia del error
nmax = iteraciones #maximo de iteraciones

def ejecutar(funcion, punto_inicial, tolerancia_error, maximo_iteraciones):
    try:
        funcion_derivada = derivar_funcion(funcion)
        console_log(LogTypes.VAR, f'f\'(x) = {funcion_derivada}')
        resultado = iterar(funcion, funcion_derivada, punto_inicial, tolerancia_error, maximo_iteraciones)
        console_print_table(resultado, ['n', 'xₙ', 'f(xₙ)', 'f\'(xₙ)', 'x⁎', 'e'])
        return resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(funcion, funcion_derivada, punto_evaluado, tolerancia_error, maximo_iteraciones):
    try:
        iteracion_actual = -1
        resultados = []
        while True:
            iteracion_actual += 1
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            imagen_punto_evaluado_derivada = evaluar_funcion(funcion_derivada, punto_evaluado)
            resultado_iteracion = calcular(punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada)
            if iteracion_actual == 0:
                resultados.append(
                    [iteracion_actual, punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada,
                     resultado_iteracion])
                punto_evaluado = resultado_iteracion
                continue
            error_relativo = calcular_error(resultado_iteracion, punto_evaluado)
            resultados.append(
                [iteracion_actual, punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada,
                 resultado_iteracion, error_relativo])
            if error_relativo < tolerancia_error or iteracion_actual >= maximo_iteraciones:
                break
            else:
                punto_evaluado = resultado_iteracion
                continue
        return resultados
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular(punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada):
    try:
        return round(float(punto_evaluado - imagen_punto_evaluado / imagen_punto_evaluado_derivada), 9)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar(fx, x, e, nmax)
