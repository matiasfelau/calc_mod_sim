import inspect
import os
from datetime import datetime, timezone, timedelta

from colorama import Style, Fore

from utiles.enumerations import LogTypes


def console_log(log_type, log_message):
    """
    Imprime un log en la terminal
    :param log_type: Elemento de utility.enumeration.LogTypes
    :param log_message:
    :return:
    """
    try:
        color = get_log_color(log_type)
        current_time = get_current_time()
        log_origin = get_log_origin()
        print(color + f'[{current_time}] {log_type}: [{log_message}] IN [{log_origin}]' + Style.RESET_ALL)
    except Exception as e:
        print(str(e))


def get_log_color(log_type):
    """
    Asigna un color al log en base a su tipo
    :param log_type:
    :return: Elemento de Fore
    """
    if log_type == LogTypes.INFO:
        return Fore.GREEN
    elif log_type == LogTypes.WARNING:
        return Fore.YELLOW
    elif log_type == LogTypes.ERROR:
        return Fore.RED
    elif log_type == LogTypes.VAR:
        return Fore.CYAN
    elif log_type == LogTypes.STATUS:
        return Fore.MAGENTA
    else:
        raise Exception(f'El tipo de log es inválido: {log_type}')


def get_current_time():
    current_time = datetime.now()  #fecha y hora del sistema
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


def get_log_origin():
    caller_frame = inspect.stack()[2] #funcion que invoca a console_log
    caller_file = caller_frame.filename #archivo de la funcion
    project_root = os.path.dirname(os.path.abspath(__file__)) #ruta al proyecto
    caller_path = os.path.relpath(caller_file, project_root) #ruta a la funcion
    caller_name = caller_frame.function #nombre de la funcion
    return f'{caller_path}::{caller_name}'