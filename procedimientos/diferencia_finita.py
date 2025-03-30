from unittest import case

from sympy.solvers.diophantine.diophantine import prime_as_sum_of_two_squares

from herramientas.analisis_matematico import evaluar_funcion
from herramientas.logger import console_log
from utiles.enumerations import LogTypes

import sympy as sp

fx = sp.sympify('sin(x)')
x = 0
h = 0.1
ord = 'primera'
orn = 'progresiva'

def ejecutar(funcion, punto_evaluado, paso, orden, orientacion):
    console_log(LogTypes.WARNING, 'SE EJECUTARA EL PROCEDIMIENTO DEL METODO DE DIFERENCIACION FINITA')
    try:
        criterio_seleccion_procedimiento = f'{orden} {orientacion}'
        console_log(LogTypes.VAR, criterio_seleccion_procedimiento)
        procedimiento = seleccionar(criterio_seleccion_procedimiento)
        resultado = procedimiento(funcion, punto_evaluado, paso)
        print(resultado)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def seleccionar(criterio):
    match criterio:
        case 'primera progresiva':
            return primer_derivada_progresiva
        case 'segunda progresiva':
            return segunda_derivada_progresiva
        case 'primera central':
            return primer_derivada_central
        case 'segunda central':
            return segunda_derivada_central
        case 'primera regresiva':
            return primer_derivada_regresiva
        case 'segunda regresiva':
            return segunda_derivada_regresiva
        case _:
            raise Exception('EL CRITERIO NO ES VALIDO')

def primer_derivada_progresiva(funcion, punto_evaluado, paso):
    return (evaluar_funcion(funcion, punto_evaluado + paso) - evaluar_funcion(funcion, punto_evaluado)) / paso

def segunda_derivada_progresiva(funcion, punto_evaluado, paso):
    return (evaluar_funcion(funcion, punto_evaluado + 2 * paso) - 2 *
            evaluar_funcion(funcion, punto_evaluado + paso) + evaluar_funcion(funcion, punto_evaluado)) / paso ** 2

def primer_derivada_central(funcion, punto_evaluado, paso):
    return ((evaluar_funcion(funcion, punto_evaluado + paso) - evaluar_funcion(funcion,punto_evaluado - paso)) /
            (2 * paso))

def segunda_derivada_central(funcion, punto_evaluado, paso):
    return (evaluar_funcion(funcion, punto_evaluado + paso) - 2 * evaluar_funcion(funcion, punto_evaluado) +
            evaluar_funcion(funcion, punto_evaluado - paso)) / paso ** 2

def primer_derivada_regresiva(funcion, punto_evaluado, paso):
    return (evaluar_funcion(funcion, punto_evaluado) - evaluar_funcion(funcion, punto_evaluado - paso)) / paso

def segunda_derivada_regresiva(funcion, punto_evaluado, paso):
    return (evaluar_funcion(funcion, punto_evaluado) - 2 * evaluar_funcion(funcion, punto_evaluado - paso) +
            evaluar_funcion(funcion, punto_evaluado - 2 * paso)) / paso ** 2

if __name__ == '__main__':
    console_log(LogTypes.STATUS, 'INICIANDO')
    ejecutar(fx, x, h, ord, orn)
    console_log(LogTypes.STATUS, 'FINALIZANDO')
