import sympy as sp

from tools.analisis_matematico import es_multiplo, evaluar_funcion, es_par, derivar_funcion, calcular_punto_maximo
from tools.logger import console_log
from tools.printer import console_print_table
from utilities.enumerations import LogTypes

fx = 'x'
a = 0
b = 1
n = 6

'''
procedimiento:
1. diferenciar si la formula a usar sera simple (n=4) o compuesta (n>4 y multiplo de 3)
si es simple:
2. calcular el paso [h=(b-a)/3]
3. reemplazar en la formula [dx=(3h/8)*(f(a)+3f(x1)+3f(x2)+f(b)), siendo m el punto medio]
si es compuesta:
2. calcular el paso [h=(b-a)/n]
3. calcular cada xi [xi=a+h*i]
4. calcular cada f(xi)
5. calcular la sumatoria de los f(xi) intermedios pares, impares y MULTIPLES DE 3
6. reemplazar en la formula [dx=3h/8*(f(a)+3*sum_impares+3*sum_pares+2*sum_multiplos_tres+f(b))]
'''
def ejecutar_metodo(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        if subdivisiones == 4:
            resultado = calcular_simple(funcion, inicio_intervalo, final_intervalo, subdivisiones)
            error_truncamiento = calcular_error_truncamiento_simple(funcion, inicio_intervalo, final_intervalo)
        elif subdivisiones > 4 and es_multiplo(subdivisiones, 3):
            tabla, resultado = calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones)
            error_truncamiento = calcular_error_truncamiento_compuesta(funcion, inicio_intervalo, final_intervalo)
            console_print_table(tabla, ['i', 'xi', 'f(xi)'])
        else:
            raise Exception('NUMERO DE SUBDIVISIONES INVALIDO')
        print(f'x* = {resultado}')
        print(f'et = {error_truncamiento}')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_simple(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        paso = (final_intervalo - inicio_intervalo) / 3
        print(f'h = {paso}')
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        primer_punto = inicio_intervalo + paso
        imagen_primer_punto = evaluar_funcion(funcion, primer_punto)
        segundo_punto = primer_punto + paso
        imagen_segundo_punto = evaluar_funcion(funcion, segundo_punto)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        return ((3 * paso) / 8) * (imagen_inicio_intervalo + 3 * imagen_primer_punto + 3 * imagen_segundo_punto + imagen_final_intervalo)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        paso = (final_intervalo - inicio_intervalo) / subdivisiones
        print(f'h = {paso}')
        tabla = []
        sumatoria_multiplos_tres = 0
        sumatoria_impares = 0
        sumatoria_pares = 0
        for iteracion in range(subdivisiones):
            punto_evaluado = inicio_intervalo + iteracion * paso
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            tabla.append([iteracion, punto_evaluado, imagen_punto_evaluado])
            if not (iteracion == 0 or iteracion == subdivisiones - 1):
                if es_multiplo(iteracion, 3):
                    sumatoria_multiplos_tres += imagen_punto_evaluado
                elif not es_par(iteracion):
                    sumatoria_impares += imagen_punto_evaluado
                else:
                    sumatoria_pares += imagen_punto_evaluado
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        resultado = ((3 * paso) / 8) * (imagen_inicio_intervalo + 3 * sumatoria_impares + 3 * sumatoria_pares + 2 * sumatoria_multiplos_tres + imagen_final_intervalo)
        return tabla, resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_truncamiento_simple(funcion, inicio_intervalo, final_intervalo):
    try:
        paso = (final_intervalo - inicio_intervalo) / 3 #todo factorizar
        punto_maximo = calcular_punto_maximo(funcion, [inicio_intervalo, final_intervalo])
        for i in range(4):
            funcion = derivar_funcion(funcion)
        epsilon = evaluar_funcion(funcion, punto_maximo)
        return - (3 / 80) * paso ** 5 * epsilon
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_truncamiento_compuesta(funcion, inicio_intervalo, final_intervalo):
    try:
        punto_maximo = calcular_punto_maximo(funcion, [inicio_intervalo, final_intervalo])
        for i in range(4):
            funcion = derivar_funcion(funcion)
        epsilon = evaluar_funcion(funcion, punto_maximo)
        return - (((final_intervalo - inicio_intervalo) ** 5) / 6480) * epsilon
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar_metodo(fx, a, b, n)