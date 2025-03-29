import sympy as sp

from herramientas.analisis_matematico import evaluar_funcion, calcular_error
from herramientas.impresion import imprimir_resultado
from herramientas.logger import console_log
from utiles.enumerations import LogTypes

x = sp.Symbol('x')

fx = x**3 - x - 2 #funcion

i = [1, 2] #intervalo

e = 0.0001 #tolerancia del error

n = 100 #maximo de iteraciones

def resolver_biseccion(funcion, intervalo, tolerancia_error, maximo_iteraciones):
    console_log(LogTypes.WARNING, 'SE EJECUTARA EL PROCEDIMIENTO DEL METODO DE BISECCION')
    inicio_intervalo = intervalo[0]
    final_intervalo = intervalo[1]
    imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
    console_log(LogTypes.VAR, f'f({inicio_intervalo}) = {imagen_inicio_intervalo}')
    imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
    console_log(LogTypes.VAR, f'f({final_intervalo}) = {imagen_final_intervalo}')
    if comprobar_bolsano(imagen_inicio_intervalo, imagen_final_intervalo):
        console_log(LogTypes.INFO, 'LA FUNCION CUMPLE CON EL TEOREMA DE BOLSANO EN EL INTERVALO')
        resultado = []
        if imagen_inicio_intervalo < 0:
            iterar(funcion, tolerancia_error, inicio_intervalo, final_intervalo, maximo_iteraciones, resultado)
        else:
            iterar(funcion, tolerancia_error, final_intervalo, inicio_intervalo, maximo_iteraciones, resultado)
        imprimir_resultado(resultado, ['n', 'x-', 'x+', 'c', 'f(c)', 'e'])
    else:
        console_log(LogTypes.WARNING, 'EL PROCEDIMIENTO SE DETENDRA PORQUE LA FUNCION NO CUMPLE CON EL TEOREMA DE BOLSANO EN EL INTERVALO')

def comprobar_bolsano(y_inicio_intervalo, y_final_intervalo):
    console_log(LogTypes.STATUS, 'COMPROBANDO')
    return y_inicio_intervalo < 0 < y_final_intervalo or y_final_intervalo < 0 < y_inicio_intervalo

def calcular_punto_medio(inicio_intervalo, final_intervalo):
    return (inicio_intervalo + final_intervalo) / 2

def iterar(funcion, tolerancia_error, extremo_negativo, extremo_positivo, maximo_iteraciones, resultado_final, resultado_anterior = 0, iteracion_actual = 0):
    if iteracion_actual == 0:
        console_log(LogTypes.STATUS, 'ITERANDO')
    punto_medio = calcular_punto_medio(extremo_negativo, extremo_positivo)
    imagen_punto_medio = evaluar_funcion(funcion, punto_medio)
    error_relativo = calcular_error(punto_medio, resultado_anterior)
    resultado_final.append(
        [iteracion_actual, extremo_negativo, extremo_positivo, punto_medio, imagen_punto_medio, error_relativo])
    if error_relativo < tolerancia_error or imagen_punto_medio == 0 or iteracion_actual >= maximo_iteraciones:
        pass
    elif imagen_punto_medio < 0:
        iterar(funcion, tolerancia_error, punto_medio, extremo_positivo, maximo_iteraciones, resultado_final, punto_medio, iteracion_actual + 1)
    elif imagen_punto_medio > 0:
        iterar(funcion, tolerancia_error, extremo_negativo, punto_medio, maximo_iteraciones, resultado_final, punto_medio, iteracion_actual + 1)

if __name__ == '__main__':
    console_log(LogTypes.STATUS, 'INICIANDO')
    resolver_biseccion(fx, i, e, n)
    console_log(LogTypes.STATUS, 'FINALIZANDO')
