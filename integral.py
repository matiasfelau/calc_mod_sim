import numpy as np
import sympy as sp
from sympy import symbols, Function, Eq, simplify, collect, solve, dsolve, exp, integrate, Integral


# Define the function to integrate directly in the code
def define_integrand():
    """Define the function to integrate directly in the code

    Returns:
        sympy expression: The function to integrate
    """
    # Define symbolic variables
    x, y = sp.symbols('x y')

    # Define your function here
    # Examples:
    # return x**2 + 3*x + 2  # ∫(x^2 + 3x + 2)dx
    # return sp.sin(x)  # ∫sin(x)dx
    # return sp.exp(x)  # ∫e^x dx
    # return x * sp.log(x)  # ∫x*ln(x)dx

    # Current function to integrate
    return sp.exp(-x) * x


def define_integration_limits():
    """Define the integration limits directly in the code

    Returns:
        tuple: (a, b) - Lower and upper limits of integration
    """
    # Define your integration limits here
    a = 0  # Lower limit
    b = 1  # Upper limit
    return a, b


def define_double_integrand():
    """Define the function for double integration directly in the code

    Returns:
        sympy expression: The function to integrate
    """
    # Define symbolic variables
    x, y = sp.symbols('x y')

    # Define your function here
    # Examples:
    # return x + y  # ∫∫(x + y)dxdy
    # return x * y  # ∫∫(x*y)dxdy
    # return x**2 + y**2  # ∫∫(x^2 + y^2)dxdy
    # return sp.sin(x) * sp.cos(y)  # ∫∫sin(x)*cos(y)dxdy

    # Current function to integrate
    return x * y


def define_double_integration_limits():
    """Define the limits for double integration directly in the code

    Returns:
        tuple: ((a, b), (c, d)) - Limits for x and y
    """
    # Define your integration limits here
    x_limits = (0, 1)  # x from 0 to 1
    y_limits = (0, 2)  # y from 0 to 2
    return x_limits, y_limits


def solve_integral_step_by_step():
    """Solve the integral and provide a step-by-step explanation"""
    # Define symbolic variables
    x = sp.symbols('x')

    # Get the integrand from the define_integrand function
    integrand = define_integrand()
    print(f"Función a integrar definida en el código: {integrand}")

    # Get integration limits
    a, b = define_integration_limits()

    print("\nPaso a paso para resolver la integral:")
    print(f"1. Tenemos la integral: ∫{integrand} dx")

    # Step 2: Identify the type of integral
    print("2. Identificando el tipo de integral:")

    # Check if it's a polynomial
    if integrand.is_polynomial(x):
        print("   Esta es una integral de un polinomio.")
        print("   Aplicamos la regla: ∫x^n dx = x^(n+1)/(n+1) + C (para n ≠ -1)")

        # Expand the polynomial
        expanded = sp.expand(integrand)
        print(f"3. Expandimos el polinomio: {expanded}")

        # Integrate term by term
        print("4. Integramos término a término:")
        terms = expanded.as_ordered_terms()
        result = 0

        for term in terms:
            term_integral = sp.integrate(term, x)
            result += term_integral
            print(f"   ∫{term} dx = {term_integral}")

        print(f"5. Sumando todos los términos: {result} + C")

        # Evaluate the definite integral if limits are provided
        if a is not None and b is not None:
            definite_result = result.subs(x, b) - result.subs(x, a)
            print(f"6. Evaluando en los límites [{a}, {b}]:")
            print(f"   {result}| entre {a} y {b} = {result.subs(x, b)} - {result.subs(x, a)} = {definite_result}")

    # Check if it's a trigonometric function
    elif any(trig_func in str(integrand) for trig_func in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc']):
        print("   Esta es una integral de una función trigonométrica.")
        print("   Aplicamos las reglas de integración trigonométrica.")

        # Integrate using sympy
        result = sp.integrate(integrand, x)
        print(f"3. Aplicando las reglas de integración: {result} + C")

        # Evaluate the definite integral if limits are provided
        if a is not None and b is not None:
            definite_result = result.subs(x, b) - result.subs(x, a)
            print(f"4. Evaluando en los límites [{a}, {b}]:")
            print(f"   {result}| entre {a} y {b} = {result.subs(x, b)} - {result.subs(x, a)} = {definite_result}")

    # Check if it's an exponential function
    elif 'exp' in str(integrand) or 'E**' in str(integrand):
        print("   Esta es una integral de una función exponencial.")
        print("   Aplicamos la regla: ∫e^x dx = e^x + C")

        # Integrate using sympy
        result = sp.integrate(integrand, x)
        print(f"3. Aplicando las reglas de integración: {result} + C")

        # Evaluate the definite integral if limits are provided
        if a is not None and b is not None:
            definite_result = result.subs(x, b) - result.subs(x, a)
            print(f"4. Evaluando en los límites [{a}, {b}]:")
            print(f"   {result}| entre {a} y {b} = {result.subs(x, b)} - {result.subs(x, a)} = {definite_result}")

    # Check if it's a logarithmic function
    elif 'log' in str(integrand) or 'ln' in str(integrand):
        print("   Esta es una integral que involucra logaritmos.")
        print("   Podemos aplicar integración por partes o reglas específicas para logaritmos.")

        # Integrate using sympy
        result = sp.integrate(integrand, x)
        print(f"3. Aplicando las reglas de integración: {result} + C")

        # Evaluate the definite integral if limits are provided
        if a is not None and b is not None:
            definite_result = result.subs(x, b) - result.subs(x, a)
            print(f"4. Evaluando en los límites [{a}, {b}]:")
            print(f"   {result}| entre {a} y {b} = {result.subs(x, b)} - {result.subs(x, a)} = {definite_result}")

    # For other types of integrals
    else:
        print("   Esta integral no se ajusta a un tipo estándar simple.")
        print("   Intentando resolver con métodos generales...")

        # Try to integrate using sympy
        try:
            result = sp.integrate(integrand, x)
            print(f"3. Resultado de la integración: {result} + C")

            # Evaluate the definite integral if limits are provided
            if a is not None and b is not None:
                definite_result = result.subs(x, b) - result.subs(x, a)
                print(f"4. Evaluando en los límites [{a}, {b}]:")
                print(f"   {result}|entre {a} y {b} = {result.subs(x, b)} - {result.subs(x, a)} = {definite_result}")
        except Exception as e:
            print(f"   Error al integrar: {e}")
            print(
                "   Esta integral puede requerir técnicas especiales o no tener una solución en términos de funciones elementales.")


def solve_double_integral_step_by_step():
    """Solve the double integral and provide a step-by-step explanation"""
    # Define symbolic variables
    x, y = sp.symbols('x y')

    # Get the integrand from the define_double_integrand function
    integrand = define_double_integrand()
    print(f"Función a integrar definida en el código: {integrand}")

    # Get integration limits
    x_limits, y_limits = define_double_integration_limits()

    print("\nPaso a paso para resolver la integral doble:")
    print(f"1. Tenemos la integral doble: ∫∫{integrand} dxdy")
    print(f"   Con límites: x ∈ [{x_limits[0]}, {x_limits[1]}], y ∈ [{y_limits[0]}, {y_limits[1]}]")

    print("2. Para resolver una integral doble, integramos primero respecto a una variable y luego respecto a la otra.")
    print("   Comenzamos integrando respecto a x:")

    # First integration with respect to x
    try:
        inner_integral = sp.integrate(integrand, (x, x_limits[0], x_limits[1]))
        print(f"3. ∫{integrand} dx (desde x={x_limits[0]} hasta x={x_limits[1]}) = {inner_integral}")

        print("4. Ahora integramos el resultado respecto a y:")

        # Second integration with respect to y
        result = sp.integrate(inner_integral, (y, y_limits[0], y_limits[1]))
        print(f"5. ∫{inner_integral} dy (desde y={y_limits[0]} hasta y={y_limits[1]}) = {result}")

        print(f"6. El resultado final de la integral doble es: {result}")

        # Alternative order of integration
        print("\nAlternativamente, podemos integrar primero respecto a y y luego respecto a x:")

        # First integration with respect to y
        alt_inner_integral = sp.integrate(integrand, (y, y_limits[0], y_limits[1]))
        print(f"7. ∫{integrand} dy (desde y={y_limits[0]} hasta y={y_limits[1]}) = {alt_inner_integral}")

        # Second integration with respect to x
        alt_result = sp.integrate(alt_inner_integral, (x, x_limits[0], x_limits[1]))
        print(f"8. ∫{alt_inner_integral} dx (desde x={x_limits[0]} hasta x={x_limits[1]}) = {alt_result}")

        print(f"9. El resultado final de la integral doble (por el método alternativo) es: {alt_result}")

        # Verify that both methods give the same result
        if sp.simplify(result - alt_result) == 0:
            print(
                "10. Verificación: Ambos métodos dan el mismo resultado, como era de esperar por el teorema de Fubini.")
        else:
            print("10. Nota: Los resultados de los dos métodos difieren numéricamente, pero deberían ser equivalentes.")

    except Exception as e:
        print(f"   Error al integrar: {e}")
        print(
            "   Esta integral puede requerir técnicas especiales o no tener una solución en términos de funciones elementales.")


if __name__ == "__main__":
    simple = True
    print(f"=== ES INTEGRAL SIMPLE?: {simple} ===")
    if simple:
        print("=== INTEGRAL SIMPLE ===")
        solve_integral_step_by_step()
    else:
        print("=== INTEGRAL DOBLE ===")
        solve_double_integral_step_by_step()
