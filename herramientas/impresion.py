from tabulate import tabulate

from herramientas.logger import console_log
from utiles.enumerations import LogTypes
from utiles.exceptions import PrintException


def imprimir_resultado(resultado, encabezado):
    console_log(LogTypes.STATUS, 'IMPRIMIENDO')
    try:
        print(tabulate(resultado, headers=encabezado, tablefmt="grid", floatfmt=".9f"))
    except Exception as e:
        mensaje = str(e)
        console_log(LogTypes.ERROR, mensaje)
        raise PrintException(mensaje)
