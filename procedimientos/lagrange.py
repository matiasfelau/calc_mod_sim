import sympy as sp

from tools.analisis_matematico import x, evaluar_funcion, derivar_funcion, calcular_punto_maximo, \
    calcular_raices_intervalo
from tools.logger import console_log
from utilities.enumerations import LogTypes

c = [[0, 0], [sp.pi/2, sp.sin(sp.pi/2)], [sp.pi, sp.sin(sp.pi)]]  # conjunto de puntos
fx = sp.sympify('sin(x)') #funcion
p = sp.pi/3
'''
procedimiento:
por cada punto xn calcular el productivo [li=(x-xi)/(xn-xi) * li], donde xi es cada punto distinto a xn
y multiplicar cada productivo por f(xn)
sumar todo
'''
def ejecutar(conjunto_puntos, funcion, punto_evaluado_error):
    try:
        resultado_crudo = iterar(conjunto_puntos)
        console_log(LogTypes.VAR, f'P(x) = {resultado_crudo}')
        resultado_final = sp.expand(resultado_crudo)
        print(f'EL POLINOMIO ES: {resultado_final}')
        error_local = calcular_error_local(funcion, resultado_final, punto_evaluado_error)
        print(f'EL ERROR LOCAL ES: {error_local}')
        error_global = calcular_error_global(funcion, conjunto_puntos)
        print(f'EL ERROR GLOBAL ES: {error_global}')
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(conjunto_puntos):
    try:
        resultado = 0
        for punto in conjunto_puntos:
            x_punto = punto[0]
            y_punto = punto[1]
            productivo = 1
            for otro_punto in conjunto_puntos:
                if otro_punto == punto:
                    continue
                x_otro_punto = otro_punto[0]
                productivo *= (x - x_otro_punto) / (x_punto - x_otro_punto)
            resultado += productivo * y_punto
        return resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular_error_local(funcion, polinomio, punto):
    try:
        return abs(evaluar_funcion(funcion, punto) - evaluar_funcion(polinomio, punto))
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

'''
procedimiento:
1. derivar la funcion inicial tantas veces como cantidad de nodos tengamos [d(x)]
2. calcular maximos y minimos de la funcion inicial
3. evaluar  en la derivada el punto con imagen mas grande de los maximos y minimos [e]
4. reemplazar el resultado del paso 3 [e] en [emax=abs(e/n!)] donde n es la cantidad de nodos
5. calcular el productivo [li=(x-xi) * li] reemplazando en xi cada punto del conjunto inicial
6. derivar el productivo
7. buscar raices en la derivada del productivo
8. evaluar la ultima raiz obtenida en la funcion productiva SIN derivar
9. multiplicar el resultado del paso 8 por emax
'''
def calcular_error_global(funcion, conjunto_puntos):
    try:
        cantidad_nodos = len(conjunto_puntos)
        derivada_funcion = funcion
        for i in range(cantidad_nodos):
            derivada_funcion = derivar_funcion(derivada_funcion)
        termino_error = derivada_funcion / sp.factorial(cantidad_nodos)
        punto_inicial = conjunto_puntos[0]
        coordenada_x_punto_inicial = punto_inicial[0]
        punto_final = conjunto_puntos[-1]
        coordenada_x_punto_final = punto_final[0]
        intervalo = [coordenada_x_punto_inicial, coordenada_x_punto_final]
        punto_maximo = calcular_punto_maximo(funcion, intervalo)
        termino_error = abs(evaluar_funcion(termino_error, punto_maximo))
        termino_productivo = 1
        for punto in conjunto_puntos:
            coordenada_x_punto = punto[0]
            termino_productivo *= (x - coordenada_x_punto)
        derivada_termino_productivo = derivar_funcion(termino_productivo)
        raices = calcular_raices_intervalo(derivada_termino_productivo, intervalo)
        ultima_raiz = raices.args[-1]
        termino_productivo = abs(evaluar_funcion(termino_productivo, ultima_raiz))
        return termino_error * termino_productivo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

if __name__ == '__main__':
    ejecutar(c, fx, p)
