import inspect
import os
from datetime import datetime

from colorama import Style, Fore

from utilities.enumerations import LogTypes


def console_log(log_type, log_message):
    try:
        log_color = get_log_color(log_type)
        current_time = get_current_time()
        log_origin = get_log_origin()
        print(log_color + f'[{current_time}] {log_type}: [{log_message}] IN [{log_origin}]' + Style.RESET_ALL)
    except Exception as e:
        print(str(e))

def get_log_color(log_type):
    match log_type:
        case LogTypes.INFO:
            return Fore.CYAN
        case LogTypes.WARNING:
            return Fore.YELLOW
        case LogTypes.ERROR:
            return Fore.RED
        case LogTypes.VAR:
            return Fore.BLUE
        case LogTypes.STATUS:
            return Fore.GREEN
        case _:
            raise Exception('TIPO DE LOG INVALIDO')

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