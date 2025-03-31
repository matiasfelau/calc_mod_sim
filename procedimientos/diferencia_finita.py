import sympy as sp

from tools.analisis_matematico import evaluar_funcion, derivar_funcion, calcular_error
from tools.logger import console_log
from utilities.enumerations import LogTypes

fx = sp.sympify('sin(x)')
x = 0
h = 0.1
ord = 'primera'
orn = 'progresiva'

def ejecutar(funcion, punto_evaluado, paso, orden, orientacion):
    try:
        criterio_seleccion_procedimiento = f'{orden} {orientacion}'
        procedimiento = seleccionar_procedimiento(criterio_seleccion_procedimiento)
        resultado_procedimiento = procedimiento(funcion, punto_evaluado, paso)
        print(f'LA DERIVADA ES: {resultado_procedimiento}')
        funcion_derivada = derivar_funcion(funcion)
        console_log(LogTypes.VAR, f'f\'(x) = {funcion_derivada}')
        resultado_absoluto = evaluar_funcion(funcion_derivada, x)
        error_absoluto = calcular_error(resultado_absoluto, resultado_procedimiento)
        print(f'EL ERROR ES: {error_absoluto}')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def seleccionar_procedimiento(criterio):
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
    try:
        return (evaluar_funcion(funcion, punto_evaluado + paso) - evaluar_funcion(funcion, punto_evaluado)) / paso
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def segunda_derivada_progresiva(funcion, punto_evaluado, paso):
    try:
        return (evaluar_funcion(funcion, punto_evaluado + 2 * paso) - 2 *
                evaluar_funcion(funcion, punto_evaluado + paso) + evaluar_funcion(funcion, punto_evaluado)) / paso ** 2
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def primer_derivada_central(funcion, punto_evaluado, paso):
    try:
        return ((evaluar_funcion(funcion, punto_evaluado + paso) - evaluar_funcion(funcion,punto_evaluado - paso)) /
                (2 * paso))
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def segunda_derivada_central(funcion, punto_evaluado, paso):
    try:
        return (evaluar_funcion(funcion, punto_evaluado + paso) - 2 * evaluar_funcion(funcion, punto_evaluado) +
                evaluar_funcion(funcion, punto_evaluado - paso)) / paso ** 2
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def primer_derivada_regresiva(funcion, punto_evaluado, paso):
    try:
        return (evaluar_funcion(funcion, punto_evaluado) - evaluar_funcion(funcion, punto_evaluado - paso)) / paso
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def segunda_derivada_regresiva(funcion, punto_evaluado, paso):
    try:
        return (evaluar_funcion(funcion, punto_evaluado) - 2 * evaluar_funcion(funcion, punto_evaluado - paso) +
                evaluar_funcion(funcion, punto_evaluado - 2 * paso)) / paso ** 2
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar(fx, x, h, ord, orn)
