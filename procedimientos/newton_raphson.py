from herramientas.analisis_matematico import derivar_funcion, evaluar_funcion, calcular_error
from herramientas.impresion import imprimir_resultado
from herramientas.logger import console_log
from utiles.enumerations import LogTypes
from utiles.exceptions import IterationException, PrintException, CheckException

import sympy as sp

fx = sp.sympify("(x - 1) ** 2") #funcion transformada
x = 0 #valor inicial
e = 1e-9 #tolerancia del error
n = 100 #maximo de iteraciones

def ejecutar(funcion, valor_inicial, tolerancia_error, maximo_iteraciones):
    console_log(LogTypes.WARNING, 'SE EJECUTARA EL PROCEDIMIENTO DEL METODO DE NEWTON RAPHSON')
    try:
        funcion_derivada = derivar_funcion(funcion)
        console_log(LogTypes.VAR, f'g\'(x) = {funcion_derivada}')
        resultado = iterar(funcion, funcion_derivada, valor_inicial, tolerancia_error, maximo_iteraciones)
        imprimir_resultado(resultado, ['n', 'xₙ', 'f(xₙ)', 'f\'(xₙ)', 'x⁎', 'e'])
    except (CheckException, IterationException, PrintException):
        pass
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(funcion, funcion_derivada, punto_evaluado, tolerancia_error, maximo_iteraciones):
    console_log(LogTypes.STATUS, 'ITERANDO')
    try:
        iteracion_actual = -1
        resultado_final = []
        while True:
            iteracion_actual += 1
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            imagen_punto_evaluado_derivada = evaluar_funcion(funcion_derivada, punto_evaluado)
            resultado_iteracion = calcular(punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada)
            if iteracion_actual == 0:
                resultado_final.append(
                    [iteracion_actual, punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada,
                     resultado_iteracion])
                punto_evaluado = resultado_iteracion
                continue
            error_relativo = calcular_error(resultado_iteracion, punto_evaluado)
            resultado_final.append(
                [iteracion_actual, punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada,
                 resultado_iteracion, error_relativo])
            if error_relativo < tolerancia_error or iteracion_actual >= maximo_iteraciones:
                break
            else:
                punto_evaluado = resultado_iteracion
                continue
        return resultado_final
    except Exception as e:
        mensaje = str(e)
        console_log(LogTypes.ERROR, mensaje)
        raise IterationException(mensaje)

def calcular(punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada):
    return punto_evaluado - imagen_punto_evaluado / imagen_punto_evaluado_derivada

if __name__ == '__main__':
    console_log(LogTypes.STATUS, 'INICIANDO')
    ejecutar(fx, x, e, n)
    console_log(LogTypes.STATUS, 'FINALIZANDO')
