import sympy as sp

from tools.analisis_matematico import x
from tools.logger import console_log
from utilities.enumerations import LogTypes

c = [[1, 1], [2, 4], [3, 9]]  # conjunto de puntos

def ejecutar(conjunto_puntos):
    try:
        resultado_crudo = iterar(conjunto_puntos)
        console_log(LogTypes.VAR, f'P(x) = {resultado_crudo}')
        resultado_final = sp.expand(resultado_crudo)
        print(f'EL POLINOMIO ES: {resultado_final}')
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

if __name__ == '__main__':
    ejecutar(c)
