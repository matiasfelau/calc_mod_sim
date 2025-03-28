import sympy as sp

from herramientas.analisis_matematico import derivar_funcion, x, evaluar_funcion, calcular_error
from herramientas.impresion import imprimir_resultado
from herramientas.logger import console_log
from utiles.enumerations import LogTypes
from utiles.exceptions import CheckException, IterationException, PrintException

gx = sp.sympify("cos(x) + x") #funcion transformada

x0 = 1 #valor inicial

e = 0.0001 #tolerancia del error

n = 100 #maximo de iteraciones

def resolver_punto_fijo(funcion_transformada, valor_inicial, tolerancia_error, maximo_iteraciones):
    console_log(LogTypes.WARNING, 'SE EJECUTARA EL PROCEDIMIENTO DE PUNTO FIJO')
    try:
        funcion_derivada = derivar_funcion(funcion_transformada)
        console_log(LogTypes.VAR, f'g\'(x) = {funcion_derivada}')
        if comprobar_contractividad(funcion_derivada, valor_inicial):
            console_log(LogTypes.INFO, 'LA FUNCION ES CONTRACTIVA')
            resultado = iterar(funcion_transformada, valor_inicial, tolerancia_error, maximo_iteraciones)
            imprimir_resultado(resultado, ['n', 'x', 'e'])
        else:
            console_log(LogTypes.WARNING, 'EL PROCEDIMIENTO SE DETENDRA PORQUE LA FUNCION NO ES CONTRACTIVA')
    except (CheckException, IterationException, PrintException):
        pass
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def comprobar_contractividad(funcion_derivada, punto_evaluado):
    console_log(LogTypes.STATUS, 'COMPROBANDO')
    try:
        return abs(funcion_derivada.subs(x, punto_evaluado)) < 1
    except Exception as e:
        mensaje = str(e)
        console_log(LogTypes.ERROR, mensaje)
        raise CheckException(mensaje)

def iterar(funcion_transformada, valor_inicial, tolerancia_error, maximo_iteraciones):
    console_log(LogTypes.STATUS, 'ITERANDO')
    try:
        iteracion_actual = 0
        punto_evaluado = valor_inicial
        resultado_final = [[iteracion_actual, valor_inicial, 'n/a']]
        while True:
            iteracion_actual += 1
            resultado_iteracion = evaluar_funcion(funcion_transformada, punto_evaluado)
            error_relativo = calcular_error(resultado_iteracion, punto_evaluado)
            resultado_final.append([iteracion_actual, resultado_iteracion, error_relativo])
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

if __name__ == '__main__':
    console_log(LogTypes.STATUS, 'INICIANDO')
    resolver_punto_fijo(gx, x0, e, n)
    console_log(LogTypes.STATUS, 'FINALIZANDO')
