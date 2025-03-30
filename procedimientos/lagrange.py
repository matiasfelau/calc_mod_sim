
import sympy as sp

from herramientas.analisis_matematico import x
from herramientas.logger import console_log
from utiles.enumerations import LogTypes
from utiles.exceptions import CheckException, IterationException, PrintException

c = [[1, 1], [2, 4], [3, 9]] #conjunto de puntos

def ejecutar(conjunto_puntos):
    console_log(LogTypes.WARNING, 'SE EJECUTARA EL PROCEDIMIENTO DEL METODO DE LAGRANGE')
    try:
        resultado_crudo = iterar(conjunto_puntos)
        console_log(LogTypes.VAR, resultado_crudo)
        resultado_final = sp.expand(resultado_crudo)
        print(resultado_final)
    except (CheckException, IterationException, PrintException):
        pass
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))

def iterar(conjunto_puntos):
    console_log(LogTypes.STATUS, 'ITERANDO')
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
        mensaje = str(e)
        console_log(LogTypes.ERROR, mensaje)
        raise IterationException(mensaje)

if __name__ == '__main__':
    console_log(LogTypes.STATUS, 'INICIANDO')
    ejecutar(c)
    console_log(LogTypes.STATUS, 'FINALIZANDO')
