import sympy as sp

from configuration import parameters as p
from tools.analisis_matematico import x, evaluar_funcion, derivar_funcion, calcular_epsilon, \
    calcular_raices
from tools.logger import console_log
from tools.plotter import plot_procedure_trajectory
from tools.printer import print_procedure_result_table
from utilities import vault as v
from utilities.enumerations import LogTypes

n = sp.Symbol('n')

c = [[0, 0], [sp.pi/2, 1], [sp.pi, 0]]  # conjunto de puntos
fx = sp.sympify('sin(x)')  #funcion #SIN
punto_error_local = sp.pi / 3


'''
procedimiento:
por cada punto xn calcular el productivo [li=(x-xi)/(xn-xi) * li], donde xi es cada punto distinto a xn
y multiplicar cada productivo por f(xn)
sumar todo
'''

def ejecutar(conjunto_puntos, funcion, punto_evaluado_error):
    try:
        print_procedure_result_table(conjunto_puntos, ['x', 'y'])
        resultado_final = iterar(conjunto_puntos)
        v.trayectoria_procedimiento += rf'$P(x)={sp.latex(resultado_final)}$' + '\n'
        if funcion is not None:
            v.trayectoria_procedimiento += rf'$|E(x)|=|f(x)-P(x)|, x={sp.latex(punto_evaluado_error)}$' + '\n'
            error_local = round(calcular_error_local(funcion, resultado_final, punto_evaluado_error), p.precision_decimales)
            v.trayectoria_procedimiento += rf'$|E(x)|={sp.latex(error_local)}$' + '\n'
            v.trayectoria_procedimiento += rf'$|E(x)| \leq M_{{n+1}}/n+1! \cdot |∏\cdot(x-x_i)|$' + '\n'
            error_global = round(calcular_error_global(funcion, conjunto_puntos), p.precision_decimales)
            v.trayectoria_procedimiento += rf'$|E(x)| \leq {error_global}$' + '\n'
            if error_local <= error_global:
                v.trayectoria_procedimiento += rf'${error_local} \leq {error_global}$' + '\n'
            else:
                v.trayectoria_procedimiento += rf'${error_local} > {error_global}$' + '\n'
        plot_procedure_trajectory('LAGRANGE', v.trayectoria_procedimiento)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def iterar(conjunto_puntos):
    try:
        iteracion = -1
        resultado = 0
        for punto in conjunto_puntos:
            iteracion += 1
            x_punto = punto[0]
            y_punto = punto[1]
            productivo = 1
            v.trayectoria_procedimiento += rf'$l_{iteracion} \cdot f(x_{iteracion}) = $'
            for otro_punto in conjunto_puntos:
                if otro_punto == punto:
                    continue
                x_otro_punto = otro_punto[0]
                v.trayectoria_procedimiento += f'(x - {x_otro_punto}) / ({x_punto} - {x_otro_punto})'
                productivo *= (x - x_otro_punto) / (x_punto - x_otro_punto)
            v.trayectoria_procedimiento += rf'$\cdot{y_punto}$' + '\n'
            v.trayectoria_procedimiento += '\n'
            resultado += productivo * y_punto
        return resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


'''
funcion - polinomio evaluado en un punto que no sea nodo
'''


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
        derivada_funcion = derivar_funcion(funcion, orden=cantidad_nodos)
        v.trayectoria_procedimiento += rf'$f^{cantidad_nodos} = {derivada_funcion}$' + '\n'
        punto_inicial = conjunto_puntos[0]
        coordenada_x_punto_inicial = punto_inicial[0]
        punto_final = conjunto_puntos[-1]
        coordenada_x_punto_final = punto_final[0]
        derivada_derivada = derivar_funcion(derivada_funcion)
        v.trayectoria_procedimiento += rf'$f^{cantidad_nodos + 1} = {derivada_derivada}$' + '\n'
        v.trayectoria_procedimiento += rf'$f^{cantidad_nodos + 1} = 0$' + '\n'
        puntos_criticos = calcular_raices(derivada_derivada, coordenada_x_punto_inicial, coordenada_x_punto_final)
        for i, punto in enumerate(puntos_criticos):
            v.trayectoria_procedimiento += rf'$x{i}={punto}$' + '\n'
            imagen_punto = evaluar_funcion(derivada_funcion, punto)
            v.trayectoria_procedimiento += rf'$f(x{i})={imagen_punto}$' + '\n'
        punto_maximo = calcular_epsilon(derivada_funcion, puntos_criticos)
        v.trayectoria_procedimiento += rf'$ε = {punto_maximo}$' + '\n'
        m = evaluar_funcion(derivada_funcion, punto_maximo)
        v.trayectoria_procedimiento += rf'$M_{{n+1}}=|f^{{n+1}}(ε)|$' + '\n'
        v.trayectoria_procedimiento += rf'$e=f^{cantidad_nodos}({punto_maximo})/{cantidad_nodos}!$' + '\n'
        termino_error = abs(evaluar_funcion(m, punto_maximo)) / sp.factorial(cantidad_nodos)
        v.trayectoria_procedimiento += rf'$e={termino_error}$' + '\n'
        termino_productivo = 1
        for punto in conjunto_puntos:
            coordenada_x_punto = punto[0]
            termino_productivo *= (x - coordenada_x_punto)
        v.trayectoria_procedimiento += rf'$|∏|={termino_productivo}$' + '\n'
        derivada_productivo = derivar_funcion(termino_productivo)
        v.trayectoria_procedimiento += rf'$∏\'={derivada_productivo}$' + '\n'
        v.trayectoria_procedimiento += rf'$∏\'=0$' + '\n'
        puntos_criticos_productivo = calcular_raices(derivada_productivo, coordenada_x_punto_inicial, coordenada_x_punto_final)
        for i, punto in enumerate(puntos_criticos_productivo):
            v.trayectoria_procedimiento += rf'$x{i}={sp.latex(punto)}$' + '\n'
            imagen_punto_productivo = evaluar_funcion(derivada_funcion, punto)
            v.trayectoria_procedimiento += rf'$f(x{i})={sp.latex(imagen_punto_productivo)}$' + '\n'
        punto_maximo_productivo = calcular_epsilon(termino_productivo, puntos_criticos_productivo)
        v.trayectoria_procedimiento += rf'$∏(ε)={punto_maximo_productivo}$' + '\n'
        termino_productivo = abs(evaluar_funcion(termino_productivo, punto_maximo_productivo))
        return termino_error * termino_productivo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


if __name__ == '__main__':
    ejecutar(c, fx, punto_error_local)
