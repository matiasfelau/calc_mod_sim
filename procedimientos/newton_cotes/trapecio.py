import sympy as sp

from tools.analisis_matematico import evaluar_funcion, derivar_funcion, calcular_epsilon, calcular_raices
from tools.logger import console_log
from tools.printer import print_procedure_result_table
from utilities.enumerations import LogTypes
from configuration import parameters as p

fx = sp.simplify('6+3*cos(x)')
a = 0
b = sp.pi/2
n = 2

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
        if subdivisiones == 1:
            resultado = calcular_simple(funcion, inicio_intervalo, final_intervalo, paso)
        elif subdivisiones > 1:
            tabla, resultado = calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones, paso)
            print_procedure_result_table(tabla, ['i', 'xi', 'f(xi)'])
        else:
            raise Exception('NUMERO DE SUBDIVISIONES INVALIDO')
        print(f'x* = {round(resultado, p.precision_decimales)}')

        error_truncamiento = calcular_error_truncamiento(funcion, inicio_intervalo, final_intervalo, subdivisiones)
        print(f'et = {round(error_truncamiento, p.precision_decimales)}')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_simple(funcion, inicio_intervalo, final_intervalo, paso):
    try:
        paso = (final_intervalo - inicio_intervalo) / 2
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        return paso * (imagen_inicio_intervalo + imagen_final_intervalo)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_compuesta(funcion, inicio_intervalo, final_intervalo, subdivisiones, paso):
    try:
        tabla = []
        sumatoria = 0
        for iteracion in range(subdivisiones + 1):
            punto_evaluado = inicio_intervalo + iteracion * paso
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            tabla.append([iteracion, punto_evaluado, imagen_punto_evaluado])
            if not (iteracion == 0 or iteracion == subdivisiones):
                sumatoria += imagen_punto_evaluado
        imagen_inicio_intervalo = evaluar_funcion(funcion, inicio_intervalo)
        imagen_final_intervalo = evaluar_funcion(funcion, final_intervalo)
        resultado = (paso / 2) * (imagen_inicio_intervalo + 2 * sumatoria + imagen_final_intervalo)
        return tabla, resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_truncamiento(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        funcion_derivada = derivar_funcion(funcion, 2)
        derivada_derivada = derivar_funcion(funcion_derivada)
        puntos_criticos = calcular_raices(derivada_derivada, inicio_intervalo, final_intervalo)
        epsilon = calcular_epsilon(funcion_derivada, puntos_criticos)
        punto_maximo = evaluar_funcion(funcion_derivada, epsilon)
        return - (((final_intervalo - inicio_intervalo) ** 3) / (12 * subdivisiones ** 2)) * punto_maximo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar_metodo(fx, a, b, n)