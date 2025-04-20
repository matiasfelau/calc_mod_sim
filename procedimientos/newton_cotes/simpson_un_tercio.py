import sympy as sp

from tools.analisis_matematico import calcular_punto_medio, evaluar_funcion, es_par, derivar_funcion, \
    calcular_epsilon, calcular_raices
from tools.logger import console_log
from tools.printer import print_procedure_result_table
from utilities.enumerations import LogTypes
from configuration import parameters as p

fx = sp.sympify('6+3*cos(x)')
a = 0
b = sp.pi/2
n = 4

'''
procedimiento:
1. diferenciar si la formula a usar sera simple (n=3) o compuesta (n>3)
si es simple:
2. calcular el paso [h=(b-a)/2]
3. reemplazar en la formula [dx=(h/3)*(f(a)+4*m+f(b)), siendo m el punto medio]
si es compuesta:
2. calcular el paso [h=(b-a)/n]
3. calcular cada xi [xi=a+h*i]
4. calcular cada f(xi)
5. calcular la sumatoria de los f(xi) intermedios pares e impares
6. reemplazar en la formula [dx=h/3*(f(a)+4*sum_impares+2*sum_pares+f(b))]
'''


def ejecutar_metodo(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        if subdivisiones == 2:
            resultado = calcular_simple(funcion, inicio_intervalo, final_intervalo)
            error_truncamiento = calcular_error_truncamiento_simple(funcion, inicio_intervalo, final_intervalo)
        elif subdivisiones > 2 and es_par(subdivisiones):
            tabla, resultado = calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones)
            print_procedure_result_table(tabla, ['i', 'xi', 'f(xi)'])
            error_truncamiento = calcular_error_truncamiento_compuesta(funcion, inicio_intervalo, final_intervalo,
                                                                       subdivisiones)
        else:
            raise Exception('NUMERO DE SUBDIVISIONES INVALIDO')
        print(f'x* = {round(resultado, p.precision_decimales)}')
        print(f'et = {round(error_truncamiento, p.precision_decimales)}')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_simple(funcion, inicio_intervalo, final_intervalo):
    try:
        paso = (final_intervalo - inicio_intervalo) / 2
        print(f'h = {paso}')
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        punto_medio = calcular_punto_medio(inicio_intervalo, final_intervalo)
        imagen_punto_medio = evaluar_funcion(funcion, punto_medio)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        return (paso / 3) * (imagen_inicio_intervalo + 4 * imagen_punto_medio + imagen_final_intervalo)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        paso = (final_intervalo - inicio_intervalo) / subdivisiones
        print(f'h = {paso}')
        tabla = []
        sumatoria_impares = 0
        sumatoria_pares = 0
        for iteracion in range(subdivisiones + 1):
            punto_evaluado = inicio_intervalo + iteracion * paso
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            tabla.append([iteracion, punto_evaluado, imagen_punto_evaluado])
            if not (iteracion == 0 or iteracion == subdivisiones):
                if not es_par(iteracion):
                    sumatoria_impares += imagen_punto_evaluado
                else:
                    sumatoria_pares += imagen_punto_evaluado
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        resultado = (paso / 3) * (
                    imagen_inicio_intervalo + 4 * sumatoria_impares + 2 * sumatoria_pares + imagen_final_intervalo)
        return tabla, resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_error_truncamiento_simple(funcion, inicio_intervalo, final_intervalo):
    try:
        funcion_derivada = derivar_funcion(funcion, 4)
        derivada_derivada = derivar_funcion(funcion_derivada)
        puntos_criticos = calcular_raices(derivada_derivada, inicio_intervalo, final_intervalo)
        epsilon = calcular_epsilon(funcion_derivada, puntos_criticos)
        punto_maximo = evaluar_funcion(funcion_derivada, epsilon)
        return - (((final_intervalo - inicio_intervalo) ** 5) / 2880) * punto_maximo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_error_truncamiento_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        paso = (final_intervalo - inicio_intervalo) / subdivisiones  #todo factorizar
        funcion_derivada = derivar_funcion(funcion, 4)
        derivada_derivada = derivar_funcion(funcion_derivada)
        puntos_criticos = calcular_raices(derivada_derivada, inicio_intervalo, final_intervalo)
        epsilon = calcular_epsilon(funcion_derivada, puntos_criticos)
        punto_maximo = evaluar_funcion(funcion_derivada, epsilon)
        return - ((final_intervalo - inicio_intervalo) / 180) * paso ** 4 * punto_maximo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


if __name__ == '__main__':
    ejecutar_metodo(fx, a, b, n)
