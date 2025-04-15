import sympy as sp

from tools.analisis_matematico import evaluar_funcion, derivar_funcion, calcular_punto_maximo
from tools.logger import console_log
from tools.printer import console_print_table
from utilities.enumerations import LogTypes

fx = sp.simplify('E^(x^2)')
a = 0
b = 1
n = 5

'''
procedimiento:
1. calcular el paso [h=(b-a)/n]
2. diferenciar si la formula a usar sera simple (n=2) o compuesta (n>2)
si es simple:
3. reemplazar en la formula [dx=h*(f(a)+f(b))]
si es compuesta:
3. calcular cada xi [xi=a+h*i]
4. calcular cada f(xi)
5. calcular la sumatoria de los f(xi) intermedios
6. reemplazar en la formula [dx=h/2*(f(a)+2*sum+f(b))]
'''
def ejecutar_metodo(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        paso = (b - a) / n
        print(f'h = {paso}')
        if subdivisiones == 2:
            resultado = calcular_simple(funcion, inicio_intervalo, final_intervalo, paso)
        elif subdivisiones > 2:
            tabla, resultado = calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones, paso)
            console_print_table(tabla, ['i', 'xi', 'f(xi)'])
        else:
            raise Exception('NUMERO DE SUBDIVISIONES INVALIDO')
        print(f'x* = {resultado}')

        error_truncamiento = calcular_error_truncamiento(funcion, inicio_intervalo, final_intervalo, subdivisiones)
        print(f'et = {error_truncamiento}')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_simple(funcion, inicio_intervalo, final_intervalo, paso):
    try:
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        return paso * (imagen_inicio_intervalo + imagen_final_intervalo)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones, paso):
    try:
        tabla = []
        sumatoria = 0
        for iteracion in range(subdivisiones):
            punto_evaluado = inicio_intervalo + iteracion * paso
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            tabla.append([iteracion, punto_evaluado, imagen_punto_evaluado])
            if not (iteracion == 0 or iteracion == subdivisiones - 1):
                sumatoria += imagen_punto_evaluado
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        resultado = (paso / 2) * (imagen_inicio_intervalo + 2 * sumatoria + imagen_final_intervalo)
        return tabla, resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_truncamiento(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        punto_maximo = calcular_punto_maximo(funcion, [inicio_intervalo, final_intervalo])
        for i in range(2):
            funcion = derivar_funcion(funcion)
        epsilon = evaluar_funcion(funcion, punto_maximo)
        return - (((final_intervalo - inicio_intervalo) ** 3) / (12 * subdivisiones ** 2)) * epsilon
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ is '__main__':
    ejecutar_metodo(fx, a, b, n)