import pytest
import sympy as sp

import procedimientos.punto_fijo as pf

import procedimientos.biseccion as bi

import procedimientos.newton_raphson as nr

from configuration.parameters import precision, tolerancia, iteraciones


def testear_punto_fijo():
    funcion = sp.sympify('cos(x) + x')
    punto_inicial = 1
    tolerancia_error = tolerancia
    maximo_iteraciones = iteraciones

    resultado_esperado = 1.570796327
    iteracion_esperada = 4

    matriz_resultado = pf.ejecutar(funcion, punto_inicial, tolerancia_error, maximo_iteraciones)

    resultado_obtenido = matriz_resultado[-1][1]
    iteracion_resultado = matriz_resultado[-1][0]

    assert pytest.approx(resultado_obtenido, abs=tolerancia_error) == resultado_esperado
    assert iteracion_resultado == iteracion_esperada

def testear_biseccion():
    funcion = sp.sympify('x**3 - x - 2')
    intervalo = [1, 2]
    tolerancia_error = tolerancia
    maximo_iteraciones = iteraciones

    resultado_esperado = 1.521379707
    iteracion_esperada = 30

    matriz_resultado = bi.ejecutar(funcion, intervalo, tolerancia_error, maximo_iteraciones)

    resultado_obtenido = matriz_resultado[-1][1]
    iteracion_resultado = matriz_resultado[-1][0]

    assert pytest.approx(resultado_obtenido, abs=tolerancia_error) == resultado_esperado
    assert iteracion_resultado == iteracion_esperada

def testear_newton_raphson():
    funcion = sp.sympify('(x - 1) ** 2')
    punto_inicial = 0
    tolerancia_error = tolerancia
    maximo_iteraciones = iteraciones

    resultado_esperado = 1
    iteracion_esperada = 30

    matriz_resultado = nr.ejecutar(funcion, punto_inicial, tolerancia_error, maximo_iteraciones)

    resultado_obtenido = matriz_resultado[-1][1]
    iteracion_resultado = matriz_resultado[-1][0]

    assert pytest.approx(resultado_obtenido, abs=tolerancia_error) == resultado_esperado
    assert iteracion_resultado == iteracion_esperada

if __name__ == '__main__':
    testear_punto_fijo()
    testear_biseccion()