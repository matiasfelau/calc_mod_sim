import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Fijar la semilla para reproducibilidad
np.random.seed(0)

# Definir la función a evaluar
def f(x, y):
    return x * np.exp(y)

# Número de puntos aleatorios
n = 10000

# Generar números aleatorios en el intervalo [0, π]
a, b = 0, 1
c, d = 1, 3
datos = np.random.uniform(a, b, n)
datos_y = np.random.uniform(c, d, n)
volumen = (b - a) * (d - c)

# Evaluar los puntos en la función
evaluados = f(datos, datos_y)

# Calcular estadísticas sobre los valores evaluados
media = np.mean(evaluados)
integral= media * volumen
desv_estandar = np.std(evaluados, ddof=1)
error_estandar = desv_estandar / np.sqrt(n)
varianza = np.var(evaluados, ddof=1)



# Visualización de resultados
plt.hist(datos, bins=50, alpha=0.6, color='b', density=True)
plt.title("Distribución de los valores generados")
plt.xlabel("x")
plt.ylabel("Frecuencia")
plt.show()

#integral estimada
print(f"Integral de f(x)")
print(f"Limite inferior a:{a}")
print(f"limite superior b:{b}")
print(f"muestras: {n}")
print("=========================================================================")

# Mostrar resultados mejorados
print(f"\nEstimación por Monte Carlo: {integral}")
print(f"\media muestral: {media}")
print(f"Valor exacto de la integral: {integral_exacta}")
print(f"Error absoluto: {abs(integral - integral_exacta)}")
print(f"Desviación estándar: {desv_estandar}")
print(f"Error estándar: {error_estandar}")
print(f"Varianza: {varianza}")
print(f"Intervalo de confianza del 95%: [{integral - 1.96 * error_estandar}, {integral + 1.96 * error_estandar}]")
print(f"Valor mínimo generado: {np.min(datos)}")
print(f"Valor máximo generado: {np.max(datos)}")

# 99,5% = 2,807
# 99% = 2,576
# 97% = 2,968
# 95% = 1,96
# 90% = 1,645
# 80% = 1,282