import sympy as sp

from tools.analisis_matematico import evaluar_funcion, calcular_punto_medio
from tools.logger import console_log
from tools.printer import console_print_table
from utilities.enumerations import LogTypes

fx = sp.simplify('E^(x^2)')
a = 0
b = 1
n = 5

def ejecutar(funcion, inicio_intervalo, final_intervalo, subdivisiones):
    try:
        paso = calcular_paso(inicio_intervalo, final_intervalo, subdivisiones)
        tabla, resultado = iterar(funcion, subdivisiones, inicio_intervalo, paso)
        console_print_table(tabla, ['i', 'xi', 'm', 'f(m)'])
        print(resultado)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_paso(inicio_intervalo, final_intervalo, iteraciones):
    try:
        return (final_intervalo - inicio_intervalo) / iteraciones
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(funcion, subdivisiones, inicio_intervalo, paso):
    try:
        resultados = []
        punto_anterior = 0
        sumatoria = 0
        for i in range(subdivisiones):
            punto = inicio_intervalo + paso * i
            if i == 0:
                resultados.append([i, punto])
                punto_anterior = punto
                continue
            punto_medio = calcular_punto_medio(punto_anterior, punto)
            imagen_punto_medio = evaluar_funcion(funcion, punto_medio)
            resultados.append([i, punto, punto_medio, imagen_punto_medio])
            sumatoria += imagen_punto_medio
            punto_anterior = punto
        sumatoria *= paso
        return resultados, sumatoria
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar(fx, a, b, n)