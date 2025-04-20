from tabulate import tabulate

from tools.logger import console_log
from utilities.enumerations import LogTypes
from configuration import parameters as p


def print_procedure_result_table(procedure_results, procedure_headers):
    try:
        print(tabulate(procedure_results, headers=procedure_headers, tablefmt='grid', floatfmt=f'.{p.precision_decimales}f'))
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))
