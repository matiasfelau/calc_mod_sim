from herramientas.analisis_matematico import derivar_funcion, evaluar_funcion, calcular_error
from herramientas.impresion import imprimir_resultado
from herramientas.logger import console_log
from procedimientos.punto_fijo import comprobar_contractividad
from utiles.enumerations import LogTypes
from utiles.exceptions import CheckException, IterationException, PrintException

import sympy as sp

gx = sp.sympify("cos(x)") #funcion transformada
x0 = 0.5 #valor inicial
e = 1e-9 #tolerancia del error
n = 100 #maximo de iteraciones

def resolver_punto_fijo_acelerado(funcion_transformada, valor_inicial, tolerancia_error, maximo_iteraciones):
    console_log(LogTypes.WARNING, 'SE EJECUTARA EL PROCEDIMIENTO DEL METODO DE PUNTO FIJO ACELERADO')
    try:
        funcion_derivada = derivar_funcion(funcion_transformada)
        console_log(LogTypes.VAR, f'g\'(x) = {funcion_derivada}')
        if comprobar_contractividad(funcion_derivada, valor_inicial):
            console_log(LogTypes.INFO, 'LA FUNCION ES CONTRACTIVA')
            resultado = iterar(funcion_transformada, valor_inicial, tolerancia_error, maximo_iteraciones)
            imprimir_resultado(resultado, ['n', 'xₙ', 'xₙ₊₁', 'xₙ₊₂', 'x⁎', 'e'])
        else:
            console_log(LogTypes.WARNING, 'EL PROCEDIMIENTO SE DETENDRA PORQUE LA FUNCION NO ES CONTRACTIVA')
    except (CheckException, IterationException, PrintException):
        pass
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(funcion_transformada, valor_inicial, tolerancia_error, maximo_iteraciones):
    console_log(LogTypes.STATUS, 'ITERANDO')
    try:
        iteracion_actual = -1
        punto_evaluado = valor_inicial
        resultado_final = []
        while True:
            iteracion_actual += 1
            segundo_punto = evaluar_funcion(funcion_transformada, punto_evaluado)
            tercer_punto = evaluar_funcion(funcion_transformada, segundo_punto)
            resultado_iteracion = acelerar(punto_evaluado, segundo_punto, tercer_punto)
            error_relativo = calcular_error(resultado_iteracion, punto_evaluado)
            resultado_final.append(
                [iteracion_actual, punto_evaluado, segundo_punto, tercer_punto, resultado_iteracion, error_relativo])
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

def acelerar(primer_punto, segundo_punto, tercer_punto):
    return primer_punto - (segundo_punto - primer_punto) ** 2 / (tercer_punto - 2 * segundo_punto + primer_punto)

if __name__ == '__main__':
    console_log(LogTypes.STATUS, 'INICIANDO')
    resolver_punto_fijo_acelerado(gx, x0, e, n)
    console_log(LogTypes.STATUS, 'FINALIZANDO')
