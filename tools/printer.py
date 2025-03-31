from tabulate import tabulate

from tools.logger import console_log
from utilities.enumerations import LogTypes


def console_print_table(data, headers):
    try:
        print(tabulate(data, headers=headers, tablefmt="grid", floatfmt=".9f"))
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))
