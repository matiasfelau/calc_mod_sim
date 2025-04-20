import sympy as sp

from tools.analisis_estadistico import calcular_valor_critico, calcular_media_muestral, calcular_desviacion_estandar, \
    calcular_error_estandar, calcular_varianza
from tools.analisis_matematico import evaluar_funcion
from tools.logger import console_log
from tools.plotter import plot_procedure_trajectory
from tools.randomizer import generar_numeros_aleatorios_uniformes, establecer_semilla
from utilities.enumerations import LogTypes
from utilities import vault as v
from configuration import parameters as p

x = sp.symbols('x')

fx = sp.sqrt(x)
a = 1  # inicio intervalo
b = 4  # final intervalo
confianza = 99  # nivel confianza
error = None  # error maximo
doble = False  # si es de doble integral el ejercicio
c = None  # inicio intervalo segunda integral
d = None  # final intervalo segunda integral
n = 5000


def ejecutar_procedimiento_monte_carlo(
        funcion,
        inicio_intervalo,
        final_intervalo,
        nivel_confianza,
        error_maximo,
        es_doble_integral,
        inicio_segundo_intervalo,
        final_segundo_intervalo,
        tamanio_muestra):
    """
    procedimiento:
    0. con una n piloto obtener s (10000)
    1. sin n calcularla [n >= ((2z*s)/e)2
    2. obtener n numeros aleatorios
    3. evaluar los numeros aleatorios
    4. obtener la media de los numeros evaluados
    5. multiplicar la media por la longitud [l=b-a para obtener la estimacion
    6. calcular el desvio estandar
    7. obtener el valor critico en base al nivel de confianza
    8. reemplazar en la formula [ic=m+-z*(s/raiz(n))
    """
    try:
        valor_critico = calcular_valor_critico(nivel_confianza)

        if tamanio_muestra is None:
            tamanio_muestra_piloto = 10000
            muestra = generar_numeros_aleatorios_uniformes(inicio_intervalo, final_intervalo, tamanio_muestra_piloto)
            muestra_evaluada = evaluar_muestra(funcion, muestra)
            desviacion_estandar = calcular_desviacion_estandar(muestra_evaluada)
            tamanio_muestra = calcular_minimo_tamanio_muestra(valor_critico, desviacion_estandar, error_maximo)

        muestra = generar_numeros_aleatorios_uniformes(inicio_intervalo, final_intervalo, tamanio_muestra)
        muestra_evaluada = evaluar_muestra(funcion, muestra)
        volumen = calcular_volumen(inicio_intervalo, final_intervalo)

        if es_doble_integral:
            segunda_muestra = generar_numeros_aleatorios_uniformes(inicio_intervalo, final_intervalo, tamanio_muestra)
            muestra_evaluada += evaluar_muestra(funcion, segunda_muestra)
            volumen *= calcular_volumen(inicio_segundo_intervalo, final_segundo_intervalo)

        media_muestral = calcular_media_muestral(muestra_evaluada)
        resultado = calcular_resultado(media_muestral, volumen)
        desviacion_estandar = calcular_desviacion_estandar(muestra_evaluada)
        error_estandar = calcular_error_estandar(desviacion_estandar, tamanio_muestra)
        varianza = calcular_varianza(muestra_evaluada)
        intervalo_confianza = calcular_intervalo_confianza(resultado, valor_critico, error_estandar)

        if not es_doble_integral:
            v.trayectoria_procedimiento += rf'$\int_{inicio_intervalo}^{final_intervalo}{sp.latex(funcion)}, dx$' + '\n'
        else:
            v.trayectoria_procedimiento += rf'$\int_{inicio_intervalo}^{final_intervalo}\int_{inicio_segundo_intervalo}^{final_segundo_intervalo}{sp.latex(funcion)}, dxdy$' + '\n'

        tamanio_muestra_formateado = sp.latex(round(tamanio_muestra, p.precision_decimales))
        resultado_formateado = sp.latex(round(resultado, p.precision_decimales))
        media_muestral_formateada = sp.latex(round(media_muestral, p.precision_decimales))
        desviacion_estandar_formateada = sp.latex(round(desviacion_estandar, p.precision_decimales))
        error_estandar_formateado = sp.latex(round(error_estandar, p.precision_decimales))
        varianza_formateada = sp.latex(round(varianza, p.precision_decimales))
        intervalo_confianza_formateado = [
            sp.latex(round(intervalo_confianza[0], p.precision_decimales)),
            sp.latex(round(intervalo_confianza[1], p.precision_decimales))]
        minimo_muestra_formateado = sp.latex(round(muestra.min(), p.precision_decimales))
        maximo_muestra_formateado = sp.latex(round(muestra.max(), p.precision_decimales))

        v.trayectoria_procedimiento += rf'$n={tamanio_muestra_formateado}$' + '\n'
        v.trayectoria_procedimiento += rf'$\bar{{x}}={media_muestral_formateada}$' + '\n'
        v.trayectoria_procedimiento += rf'$s={desviacion_estandar_formateada}$' + '\n'
        v.trayectoria_procedimiento += '\n'
        if es_doble_integral:
            v.trayectoria_procedimiento += rf'$\hat{{I}} = {media_muestral_formateada}\cdot (({final_intervalo}+ {inicio_intervalo})\cdot ({final_segundo_intervalo}+ {inicio_segundo_intervalo}))$' + '\n'
        else:
            v.trayectoria_procedimiento += rf'$\hat{{I}} = {media_muestral_formateada}\cdot ({final_intervalo}+ {inicio_intervalo})$' + '\n'
        v.trayectoria_procedimiento += rf'$\hat{{I}}={resultado_formateado}$' + '\n'
        v.trayectoria_procedimiento += '\n'
        v.trayectoria_procedimiento += rf'$EE=\frac{{{desviacion_estandar_formateada}}}{{\sqrt{{{tamanio_muestra_formateado}}}}}$' + '\n'
        v.trayectoria_procedimiento += rf'$EE={error_estandar_formateado}$' + '\n'
        v.trayectoria_procedimiento += rf'$s^2={varianza_formateada}$' + '\n'
        v.trayectoria_procedimiento += '\n'
        v.trayectoria_procedimiento += rf'$I_{{{nivel_confianza}}}=[{resultado_formateado} - Z_{{{nivel_confianza}}}\cdot{error_estandar_formateado}; {resultado_formateado} + Z_{{{nivel_confianza}}}\cdot{error_estandar_formateado}]$' + '\n'
        v.trayectoria_procedimiento += rf'$I_{{{nivel_confianza}}}={intervalo_confianza_formateado}$' + '\n'
        v.trayectoria_procedimiento += rf'$n_{{min}}={minimo_muestra_formateado}$' + '\n'
        v.trayectoria_procedimiento += rf'$n_{{max}}={maximo_muestra_formateado}$' + '\n'
        plot_procedure_trajectory('MONTE CARLO', v.trayectoria_procedimiento)
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_volumen(inicio_intervalo, final_intervalo):
    try:
        return final_intervalo - inicio_intervalo
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_resultado(media_muestral, volumen):
    try:
        return media_muestral * volumen
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def evaluar_muestra(funcion, muestra):
    try:
        return [float(evaluar_funcion(funcion, punto)) for punto in muestra]
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_minimo_tamanio_muestra(valor_critico, desviacion_estandar, error_maximo):
    try:
        return (error_maximo ** -1 * 2 * valor_critico * desviacion_estandar) ** 2
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


def calcular_intervalo_confianza(resultado, valor_critico, error_estandar):
    try:
        return [(resultado - valor_critico * error_estandar), (resultado + valor_critico * error_estandar)]
    except Exception as e:
        console_log(LogTypes.ERROR, str(e))


if __name__ == '__main__':
    establecer_semilla(0)
    ejecutar_procedimiento_monte_carlo(fx, a, b, confianza, error, doble, c, d, n)
