import sympy as sp

from configuration.parameters import tolerancia, iteraciones
from tools.analisis_matematico import evaluar_funcion, calcular_error
from tools.logger import console_log
from tools.printer import console_print_table
from utilities.enumerations import LogTypes

x = sp.Symbol('x')

fx = sp.sympify("x**3 - x - 2") #funcion
i = [1, 2] #intervalo
e = tolerancia #tolerancia del error #todo
nmax = iteraciones #maximo de iteraciones

def ejecutar(funcion, intervalo, tolerancia_error, maximo_iteraciones):
    try:
        inicio_intervalo = intervalo[0]
        final_intervalo = intervalo[1]
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        console_log(LogTypes.VAR, f'f({inicio_intervalo}) = {imagen_inicio_intervalo}')
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        console_log(LogTypes.VAR, f'f({final_intervalo}) = {imagen_final_intervalo}')
        if comprobar_bolsano(imagen_inicio_intervalo, imagen_final_intervalo):
            if imagen_inicio_intervalo < 0:
                resultados = iterar(funcion, tolerancia_error, inicio_intervalo, final_intervalo, maximo_iteraciones)
            else:
                resultados = iterar(funcion, tolerancia_error, final_intervalo, inicio_intervalo, maximo_iteraciones)
            console_print_table(resultados, ['n', 'x-', 'x+', 'c', 'f(c)', 'e'])
            return resultados
        else:
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

def iterar(funcion, tolerancia_error, extremo_negativo, extremo_positivo, maximo_iteraciones):
    try:
        iteracion_actual = -1
        resultados = []
        resultado_anterior = None
        while True:
            iteracion_actual += 1
            punto_medio = calcular_punto_medio(extremo_negativo, extremo_positivo)
            imagen_punto_medio = evaluar_funcion(funcion, punto_medio)
            if iteracion_actual == 0:
                resultados.append([iteracion_actual, extremo_negativo, extremo_positivo, punto_medio, imagen_punto_medio])
            else:
                error_relativo = calcular_error(punto_medio, resultado_anterior)
                resultados.append(
                    [iteracion_actual, extremo_negativo, extremo_positivo, punto_medio, imagen_punto_medio, error_relativo])
                if error_relativo < tolerancia_error or iteracion_actual >= maximo_iteraciones:
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
    ejecutar(fx, i, e, nmax)
