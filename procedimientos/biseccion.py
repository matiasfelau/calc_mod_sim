import sympy as sp

from tools.analisis_matematico import evaluar_funcion, calcular_error_relativo
from tools.logger import console_log
from tools.plotter import plot_procedure_trajectory
from tools.printer import print_procedure_result_table
from utilities.enumerations import LogTypes
from utilities import vault as v
from configuration import parameters as p

x = sp.Symbol('x')

fx = sp.sympify("x**3 - x - 2")  #funcion
i = [1, 2]  #intervalo

'''
procedimiento:
1. evaluar cada extremo del intervalo en la funcion
2. verificar que cumple el teorema de bolsano (ambos extremos tienen imagenes opuestas)
3. calcular el punto medio del intervalo [m=(a+b)/2]
4. evaluar el punto medio en la funcion
iteracion:
5. reemplazar el punto medio en el extremo con mismo signo en sus imagenes
6. calcular el punto medio del nuevo intervalo
'''


def ejecutar(funcion, intervalo):
    try:
        v.trayectoria_procedimiento += rf'$f(x) = {sp.latex(funcion)}, i={intervalo}$' + '\n'
        inicio_intervalo = intervalo[0]
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        v.trayectoria_procedimiento += rf'$f({inicio_intervalo}) = {imagen_inicio_intervalo}$' + '\n'
        final_intervalo = intervalo[1]
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        v.trayectoria_procedimiento += rf'$f({final_intervalo}) = {imagen_final_intervalo}$' + '\n'
        if comprobar_bolsano(imagen_inicio_intervalo, imagen_final_intervalo):
            v.trayectoria_procedimiento += rf'$f({inicio_intervalo}) * f({final_intervalo}) < 0$' + '\n'
            if imagen_inicio_intervalo < 0:
                resultados = iterar(funcion, inicio_intervalo, final_intervalo)
            else:
                resultados = iterar(funcion, final_intervalo, inicio_intervalo)
            plot_procedure_trajectory('BISECCION', v.trayectoria_procedimiento)
            print_procedure_result_table(resultados, ['n', 'x-', 'x+', 'c', 'f(c)', 'e'])
            return resultados
        else:
            v.trayectoria_procedimiento += rf'$f({inicio_intervalo}) * f({final_intervalo}) >= 0$' + '\n'

            v.trayectoria_procedimiento += 'NO CUMPLE BOLSANO' + '\n'
            console_log(LogTypes.WARNING, 'LA FUNCION NO CUMPLE CON EL TEOREMA DE BOLSANO')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def comprobar_bolsano(y_inicio_intervalo, y_final_intervalo):
    try:
        return y_inicio_intervalo < 0 < y_final_intervalo or y_final_intervalo < 0 < y_inicio_intervalo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_punto_medio(inicio_intervalo, final_intervalo):
    try:
        return (inicio_intervalo + final_intervalo) / 2
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def iterar(funcion, extremo_negativo, extremo_positivo):
    try:
        iteracion_actual = -1
        resultados = []
        resultado_anterior = None
        while True:
            iteracion_actual += 1
            punto_medio = calcular_punto_medio(extremo_negativo, extremo_positivo)
            imagen_punto_medio = evaluar_funcion(funcion, punto_medio)
            if iteracion_actual == 0:
                resultados.append(
                    [iteracion_actual, extremo_negativo, extremo_positivo, punto_medio, imagen_punto_medio])
            else:
                error_relativo = calcular_error_relativo(punto_medio, resultado_anterior)
                resultados.append(
                    [iteracion_actual, extremo_negativo, extremo_positivo, punto_medio, imagen_punto_medio,
                     error_relativo])
                if error_relativo < p.tolerancia_error or iteracion_actual >= p.maximo_iteraciones:
                    v.trayectoria_procedimiento += rf'$x^* = {punto_medio:.{p.precision_decimales}f}, n = {iteracion_actual}$' + '\n'
                    break
            resultado_anterior = punto_medio
            if imagen_punto_medio == 0:
                break
            elif imagen_punto_medio < 0:
                extremo_negativo = punto_medio
                continue
            elif imagen_punto_medio > 0:
                extremo_positivo = punto_medio
                continue
        return resultados
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


if __name__ == '__main__':
    ejecutar(fx, i)
