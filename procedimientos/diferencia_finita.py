import sympy as sp

from configuration import parameters as p
from tools.plotter import plot_procedure_trajectory
from utilities import vault as v
from tools.analisis_matematico import evaluar_funcion, derivar_funcion, calcular_error_relativo
from tools.logger import console_log
from utilities.enumerations import LogTypes

fx = sp.sympify('sin(x)')
x = 0
h = 0.1
ord = 'primera'
orn = 'progresiva'

def ejecutar(funcion, punto_evaluado, paso, orden, orientacion):
    try:
        if orden == 'primera':
            i_orden = 1
        else:
            i_orden = 2
        criterio_seleccion_procedimiento = f'{orden} {orientacion}'
        procedimiento = seleccionar_procedimiento(criterio_seleccion_procedimiento)
        resultado_procedimiento = round(procedimiento(funcion, punto_evaluado, paso), p.precision_decimales)

        v.trayectoria_procedimiento += rf'$f^{i_orden}={sp.latex(resultado_procedimiento)}$' + '\n'
        funcion_derivada = funcion
        for i in range(i_orden):
            funcion_derivada = derivar_funcion(funcion_derivada)
        v.trayectoria_procedimiento += rf'$f^{i_orden}={sp.latex(funcion_derivada)}$' + '\n'
        resultado_absoluto = evaluar_funcion(funcion_derivada, x)

        v.trayectoria_procedimiento += rf'$f^{i_orden}({punto_evaluado})={sp.latex(resultado_absoluto)}$' + '\n'
        error_absoluto = calcular_error_relativo(resultado_absoluto, resultado_procedimiento)
        v.trayectoria_procedimiento += rf'$E_{{abs}}={error_absoluto}$' + '\n'
        plot_procedure_trajectory('DIFERENCIA FINITA', v.trayectoria_procedimiento)
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
