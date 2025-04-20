import pytest
import sympy as sp

import procedimientos.punto_fijo as pf

import procedimientos.biseccion as bi

import procedimientos.newton_raphson as nr

from configuration import parameters as p


def test_punto_fijo():
    funcion = sp.sympify('cos(x) + x')
    punto_inicial = 1

    resultado_esperado = 1.570796327
    iteracion_esperada = 4

    matriz_resultado = pf.iterar(funcion, punto_inicial)

    resultado_obtenido = matriz_resultado[-1][1]
    iteracion_resultado = matriz_resultado[-1][0]

    assert pytest.approx(resultado_esperado, p.tolerancia_error) == resultado_obtenido
    assert iteracion_resultado == iteracion_esperada


def test_biseccion():
    funcion = sp.sympify('x**3 - x - 2')
    a = 1
    b = 2

    resultado_esperado = 1.521379706
    iteracion_esperada = 29

    matriz_resultado = bi.iterar(funcion, a, b)

    resultado_obtenido = matriz_resultado[-1][1]
    iteracion_resultado = matriz_resultado[-1][0]

    assert pytest.approx(resultado_esperado, p.tolerancia_error) == resultado_obtenido
    assert iteracion_resultado == iteracion_esperada


def test_newton_raphson():
    funcion = sp.sympify('(x - 1) ** 2')
    derivada = sp.sympify('2 * x - 2')
    punto_inicial = 0

    resultado_esperado = 0.999999999
    iteracion_esperada = 29

    matriz_resultado = nr.iterar(funcion, derivada, punto_inicial)

    resultado_obtenido = matriz_resultado[-1][1]
    iteracion_resultado = matriz_resultado[-1][0]

    assert pytest.approx(resultado_esperado, p.tolerancia_error) == resultado_obtenido
    assert iteracion_resultado == iteracion_esperada
