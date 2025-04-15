import sympy as sp

from tools.analisis_matematico import calcular_punto_medio, evaluar_funcion, es_par, derivar_funcion, \
    calcular_punto_maximo
from tools.logger import console_log
from tools.printer import console_print_table
from utilities.enumerations import LogTypes

fx = 'x'
a = 0
b = 1
n = 3

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
        if subdivisiones == 3:
            resultado = calcular_simple(funcion, inicio_intervalo, final_intervalo)
            error_truncamiento = calcular_error_truncamiento_simple(funcion, inicio_intervalo, final_intervalo)
        elif subdivisiones > 3 and es_par(subdivisiones):
            tabla, resultado = calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones)
            console_print_table(tabla, ['i', 'xi', 'f(xi)'])
            error_truncamiento = calcular_error_truncamiento_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones)
        else:
            raise Exception('NUMERO DE SUBDIVISIONES INVALIDO')
        print(f'x* = {resultado}')
        print(f'et = {error_truncamiento}')
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
        for iteracion in range(subdivisiones):
            punto_evaluado = inicio_intervalo + iteracion * paso
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            tabla.append([iteracion, punto_evaluado, imagen_punto_evaluado])
            if not (iteracion == 0 or iteracion == subdivisiones - 1):
                if not es_par(iteracion):
                    sumatoria_impares += imagen_punto_evaluado
                else:
                    sumatoria_pares += imagen_punto_evaluado
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        resultado = (paso / 3) * (imagen_inicio_intervalo + 4 * sumatoria_impares + 2 * sumatoria_pares + imagen_final_intervalo)
        return tabla, resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_truncamiento_simple(funcion, inicio_intervalo, final_intervalo):
    try:
        for i in range(4):
            funcion = derivar_funcion(funcion)
        punto_maximo = calcular_punto_maximo(funcion, [inicio_intervalo, final_intervalo])
        epsilon = evaluar_funcion(funcion, punto_maximo)
        return - (((final_intervalo - inicio_intervalo) ** 5) / 2880) * epsilon
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_truncamiento_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        paso = (final_intervalo - inicio_intervalo) / subdivisiones #todo factorizar
        punto_maximo = calcular_punto_maximo(funcion, [inicio_intervalo, final_intervalo])
        for i in range(4):
            funcion = derivar_funcion(funcion)
        epsilon = evaluar_funcion(funcion, punto_maximo)
        return - ((final_intervalo - inicio_intervalo) / 180) * paso ** 4 * epsilon
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar_metodo(fx, a, b, n)