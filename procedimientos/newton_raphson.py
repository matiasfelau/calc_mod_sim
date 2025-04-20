import sympy as sp

from tools.plotter import plot_procedure_trajectory
from utilities import vault as v
from configuration import parameters as p
from tools.analisis_matematico import derivar_funcion, evaluar_funcion, calcular_error_relativo
from tools.logger import console_log
from tools.printer import print_procedure_result_table
from utilities.enumerations import LogTypes

fx = sp.sympify("(x - 1) ** 2") #funcion
x = 0 #punto inicial

'''
procedimiento:
1. derivar la funcion
iteracion:
2. evaluar el punto en la funcion
3. evaluar el mismo punto en la funcion derivada
4. reemplazar en la formula [x*=xn-f(n)/f'(n)
'''
def ejecutar(funcion, punto_inicial):
    try:
        v.trayectoria_procedimiento += rf'$f(x)={sp.latex(funcion)}, x_0={punto_inicial}$' + '\n'
        funcion_derivada = derivar_funcion(funcion)
        v.trayectoria_procedimiento += rf'$f\'(x) = {sp.latex(funcion_derivada)}$' + '\n'
        resultado = iterar(funcion, funcion_derivada, punto_inicial)
        plot_procedure_trajectory('NEWTON RAPHSON', v.trayectoria_procedimiento)
        print_procedure_result_table(resultado, ['n', 'xₙ', 'f(xₙ)', 'f\'(xₙ)', 'x⁎', 'e'])
        return resultado
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(funcion, funcion_derivada, punto_evaluado):
    try:
        iteracion_actual = -1
        resultados = []
        while True:
            iteracion_actual += 1
            imagen_punto_evaluado = evaluar_funcion(funcion, punto_evaluado)
            imagen_punto_evaluado_derivada = evaluar_funcion(funcion_derivada, punto_evaluado)
            try:
                resultado_iteracion = calcular(punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada)
            except ZeroDivisionError:
                v.trayectoria_procedimiento += rf'$x^*={punto_evaluado}, n={iteracion_actual - 1}' + '\n'
                console_log(LogTypes.WARNING, f'DIVISION POR CERO A PARTIR DE ITERACION {iteracion_actual - 1}')
                break
            if iteracion_actual == 0:
                resultados.append([
                    iteracion_actual,
                    punto_evaluado,
                    imagen_punto_evaluado,
                    imagen_punto_evaluado_derivada,
                    resultado_iteracion])
                punto_evaluado = resultado_iteracion
                continue
            error_relativo = calcular_error_relativo(resultado_iteracion, punto_evaluado)
            resultados.append([
                iteracion_actual,
                punto_evaluado,
                imagen_punto_evaluado,
                imagen_punto_evaluado_derivada,
                resultado_iteracion,
                error_relativo])
            if error_relativo < p.tolerancia_error or iteracion_actual >= p.maximo_iteraciones:
                v.trayectoria_procedimiento += rf'$x^*={f'{resultado_iteracion:.{p.precision_decimales}f}'},n={iteracion_actual}$' + '\n'
                break
            else:
                punto_evaluado = resultado_iteracion
                continue
        return resultados
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def calcular(punto_evaluado, imagen_punto_evaluado, imagen_punto_evaluado_derivada):
    if imagen_punto_evaluado_derivada != 0:
        return punto_evaluado - imagen_punto_evaluado / imagen_punto_evaluado_derivada
    else:
        raise ZeroDivisionError

if __name__ == '__main__':
    ejecutar(fx, x)
