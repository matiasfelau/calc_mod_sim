import numpy as np
from tools.logger import console_log
from utilities.enumerations import LogTypes


def establecer_semilla(valor):
    try:
        np.random.seed(valor)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def generar_numeros_aleatorios_uniformes(minimo, maximo, cantidad):
    try:
        return np.random.uniform(minimo, maximo, cantidad)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))
