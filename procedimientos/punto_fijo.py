import numpy as np
import sympy as sp

from configuration import parameters as p
from tools.analisis_matematico import derivar_funcion, x, evaluar_funcion, calcular_error_relativo
from tools.logger import console_log
from tools.plotter import plot_procedure_trajectory
from tools.printer import print_procedure_result_table
from utilities import vault as v
from utilities.enumerations import LogTypes

gx = sp.sympify("cos(x) + x")  #funcion transformada #cos(x)
x0 = 1  #punto inicial #0.5
aitken = False

'''
para transformar:
si es una elemental como cosx sumarle x
si es un polinomio despejar x, si no se contrae separar por ej x^2= x*x y despejar
procedimiento:
1. despejar la funcion para encontrar una funcion auxiliar g(x)
2. verificar que la funcion converge [abs(g'(x)) < 1]
3. evaluar en la funcion el punto inicial
iteracion: 
4. evaluar en la funcion el resultado de la iteracion anterior
'''
'''
procedimiento aitken:
1. despejar la funcion para encontrar una funcion auxiliar g(x)
2. verificar que la funcion converge [abs(g'(x)) < 1]
iteracion:
3. evaluar el punto inicial en la funcion
4. evaluar el siguiente punto en la funcion [xn+1]
5. evaluar el siguiente punto en la funcion [xn+2]
6. reemplazar en la formula [x*=xn-((xn+1-xn)^2)/(xn+2-2*xn+1-xn]
'''

def f(x):
    return np.cos(x) + x


def ejecutar_procedimiento_punto_fijo(funcion_transformada, punto_inicial, es_acelerado):
    try:
        v.trayectoria_procedimiento += rf'$g(x) = {sp.latex(funcion_transformada)}, x_0={punto_inicial}, $' + '\n'
        funcion_derivada = derivar_funcion(funcion_transformada)
        v.trayectoria_procedimiento += rf'$g\'(x) = {sp.latex(funcion_derivada)}$' + '\n'
        if comprobar_contractividad(funcion_derivada, punto_inicial):
            if not es_acelerado:
                nombre_procedimiento = 'PUNTO FIJO'
                resultados_procedimiento = iterar(funcion_transformada, punto_inicial)
                encabezados_tabla_procedimiento = ['n', 'x', 'e']
            else:
                nombre_procedimiento = 'PUNTO FIJO ACELERADO'
                resultados_procedimiento = iterar_aceleracion(funcion_transformada, punto_inicial)
                encabezados_tabla_procedimiento = ['n', 'xₙ', 'xₙ₊₁', 'xₙ₊₂', 'x⁎', 'e']
            plot_procedure_trajectory(nombre_procedimiento, v.trayectoria_procedimiento)
            print_procedure_result_table(resultados_procedimiento, encabezados_tabla_procedimiento)
            return resultados_procedimiento
        else:
            console_log(LogTypes.WARNING, 'LA FUNCION NO ES CONTRACTIVA')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def comprobar_contractividad(funcion_derivada, punto):
    try:
        v.trayectoria_procedimiento += rf'$|g\'(x_0)| < 1$' + '\n'
        resultado = abs(evaluar_funcion(funcion_derivada, punto))
        es_contractiva = resultado < 1
        if es_contractiva:
            v.trayectoria_procedimiento += rf'${sp.latex(resultado)} < 1$' + '\n'
        else:
            v.trayectoria_procedimiento += rf'${sp.latex(resultado)} >= 1$' + '\n'
            v.trayectoria_procedimiento += rf'$NO ES CONTRACTIVA$' + '\n'
        return es_contractiva
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def iterar(funcion_transformada, punto_evaluado):
    try:
        iteracion_actual = -1
        resultados = []
        while True:
            iteracion_actual += 1
            if iteracion_actual == 0:
                resultados.append([iteracion_actual, punto_evaluado])
                continue
            resultado_iteracion = evaluar_funcion(funcion_transformada, punto_evaluado)
            error_relativo = calcular_error_relativo(resultado_iteracion, punto_evaluado)
            resultados.append([iteracion_actual,
                               resultado_iteracion,
                               error_relativo])
            if error_relativo < p.tolerancia_error or iteracion_actual >= p.maximo_iteraciones:
                v.trayectoria_procedimiento += rf'$x^* = {resultado_iteracion:.{p.precision_decimales}f}, n = {iteracion_actual}$' + '\n'
                break
            else:
                punto_evaluado = resultado_iteracion
                continue
        return resultados
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def iterar_aceleracion(funcion_transformada, punto_evaluado):
    try:
        iteracion_actual = -1
        resultados = []
        while True:
            iteracion_actual += 1
            segundo_punto = evaluar_funcion(funcion_transformada, punto_evaluado)
            tercer_punto = evaluar_funcion(funcion_transformada, segundo_punto)
            try:
                resultado_iteracion = acelerar(punto_evaluado, segundo_punto, tercer_punto)
            except ZeroDivisionError:
                v.trayectoria_procedimiento += rf'$x^* = {punto_evaluado:.{p.precision_decimales}f}, n = {iteracion_actual - 1}$' + '\n'
                console_log(LogTypes.WARNING, f'DIVISION POR CERO A PARTIR DE ITERACION {iteracion_actual - 1}')
                break
            if iteracion_actual == 0:
                resultados.append([
                    iteracion_actual,
                    punto_evaluado,
                    segundo_punto,
                    tercer_punto,
                    resultado_iteracion])
                punto_evaluado = resultado_iteracion
                continue
            error_relativo = calcular_error_relativo(resultado_iteracion, punto_evaluado)
            resultados.append([
                iteracion_actual,
                punto_evaluado,
                segundo_punto,
                tercer_punto,
                resultado_iteracion,
                error_relativo])
            if error_relativo < p.tolerancia_error or iteracion_actual >= p.maximo_iteraciones:
                v.trayectoria_procedimiento += rf'$x^* = {resultado_iteracion:.{p.precision_decimales}f}, n = {iteracion_actual}$' + '\n'
                break
            else:
                punto_evaluado = resultado_iteracion
                continue
        return resultados
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def acelerar(primer_punto, segundo_punto, tercer_punto):
    denominador = (tercer_punto - 2 * segundo_punto + primer_punto)
    if denominador != 0:
        return primer_punto - (segundo_punto - primer_punto) ** 2 / denominador
    else:
        raise ZeroDivisionError


if __name__ == '__main__':
    ejecutar_procedimiento_punto_fijo(gx, x0, aitken)
