import numpy as np
from scipy.stats import norm

from tools.logger import console_log
from utilities.enumerations import LogTypes


def calcular_valor_critico(nivel_confianza):
    try:
        return norm.ppf(1 - (1 - nivel_confianza / 100) / 2)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_desviacion_estandar(muestra):
    try:
        return np.std(muestra, ddof=1)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_error_estandar(desviacion_estandar, tamanio_muestra):
    try:
        return desviacion_estandar / np.sqrt(tamanio_muestra)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_media_muestral(muestra):
    try:
        return np.mean(muestra)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_varianza(muestra):
    try:
        return np.var(muestra, ddof=1)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))
