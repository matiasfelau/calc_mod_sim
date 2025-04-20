import sympy as sp

from tools.analisis_matematico import es_multiplo, evaluar_funcion, es_par, derivar_funcion, calcular_epsilon, \
    calcular_raices
from tools.logger import console_log
from tools.printer import print_procedure_result_table
from utilities.enumerations import LogTypes
from configuration import parameters as p

fx = sp.sympify('6+3*cos(x)')
a = 0
b = sp.pi/2
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
        if subdivisiones == 3:
            resultado = calcular_simple(funcion, inicio_intervalo, final_intervalo, subdivisiones)
            error_truncamiento = calcular_error_truncamiento_simple(funcion, inicio_intervalo, final_intervalo)
        elif subdivisiones > 3 and es_multiplo(subdivisiones, 3):
            tabla, resultado = calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones)
            error_truncamiento = calcular_error_truncamiento_compuesta(funcion, inicio_intervalo, final_intervalo)
            print_procedure_result_table(tabla, ['i', 'xi', 'f(xi)'])
        else:
            raise Exception('NUMERO DE SUBDIVISIONES INVALIDO')
        print(f'x* = {round(resultado, p.precision_decimales)}')
        print(f'et = {round(error_truncamiento, p.precision_decimales)}')
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
        for iteracion in range(subdivisiones + 1):
            punto_evaluado = inicio_intervalo + iteracion * paso
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            tabla.append([iteracion, punto_evaluado, imagen_punto_evaluado])
            if not (iteracion == 0 or iteracion == subdivisiones):
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
        funcion_derivada = derivar_funcion(funcion, 4)
        derivada_derivada = derivar_funcion(funcion_derivada)
        puntos_criticos = calcular_raices(derivada_derivada, inicio_intervalo, final_intervalo)
        epsilon = calcular_epsilon(funcion_derivada, puntos_criticos)
        punto_maximo = evaluar_funcion(funcion_derivada, epsilon)
        return - (3 / 80) * paso ** 5 * punto_maximo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_truncamiento_compuesta(funcion, inicio_intervalo, final_intervalo):
    try:
        funcion_derivada = derivar_funcion(funcion, 4)
        derivada_derivada = derivar_funcion(funcion_derivada)
        puntos_criticos = calcular_raices(derivada_derivada, inicio_intervalo, final_intervalo)
        epsilon = calcular_epsilon(funcion_derivada, puntos_criticos)
        punto_maximo = evaluar_funcion(funcion_derivada, epsilon)
        return - (((final_intervalo - inicio_intervalo) ** 5) / 6480) * punto_maximo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar_metodo(fx, a, b, n)