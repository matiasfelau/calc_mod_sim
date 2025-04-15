import sympy as sp

from configuration.parameters import tolerancia, iteraciones
from tools.analisis_matematico import derivar_funcion, x, evaluar_funcion, calcular_error
from tools.logger import console_log
from tools.printer import console_print_table
from utilities.enumerations import LogTypes

gx = sp.sympify("cos(x) + x") #funcion transformada
x0 = 1 #punto inicial
e = tolerancia #tolerancia del error
nmax = iteraciones #maximo de iteraciones

def ejecutar(funcion_transformada, punto_inicial, tolerancia_error, maximo_iteraciones):
    try:
        funcion_derivada = derivar_funcion(funcion_transformada)
        console_log(LogTypes.VAR, f'g\'(x) = {funcion_derivada}')
        if comprobar_contractividad(funcion_derivada, punto_inicial):
            resultados = iterar(funcion_transformada, punto_inicial, tolerancia_error, maximo_iteraciones)
            console_print_table(resultados, ['n', 'x', 'e'])
            return resultados
        else:
            console_log(LogTypes.WARNING, 'LA FUNCION NO ES CONTRACTIVA')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def comprobar_contractividad(funcion_derivada, punto_evaluado):
    try:
        return abs(funcion_derivada.subs(x, punto_evaluado)) < 1
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(funcion_transformada, punto_evaluado, tolerancia_error, maximo_iteraciones):
    try:
        iteracion_actual = -1
        resultados = []
        while True:
            iteracion_actual += 1
            if iteracion_actual == 0:
                resultados.append([iteracion_actual, punto_evaluado])
                continue
            resultado_iteracion = evaluar_funcion(funcion_transformada, punto_evaluado)
            error_relativo = calcular_error(resultado_iteracion, punto_evaluado)
            resultados.append([iteracion_actual, resultado_iteracion, error_relativo])
            if error_relativo < tolerancia_error or iteracion_actual >= maximo_iteraciones:
                break
            else:
                punto_evaluado = resultado_iteracion
                continue
        return resultados
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar(gx, x0, e, nmax)
