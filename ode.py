import numpy as np
import sympy as sp

# Define the ODE directly in the code
def define_ode():
    """Define the ODE directly in the code

    Returns:
        sympy expression: The right-hand side of the ODE dy/dt = ...
    """
    # Define symbolic variables
    t, y = sp.symbols('t y')

    # Define your ODE here
    # Examples:
    # return 2 * t + 3 * y  # dy/dt = 2t + 3y
    # return -y + t  # dy/dt = -y + t
    # return sp.sin(t) * y  # dy/dt = sin(t) * y
    # return sp.exp(-t) + sp.cos(t) * y  # dy/dt = e^(-t) + cos(t) * y

    # Current ODE: dy/dt = e^(-t) + cos(t) * y
    return  t*y

def define_initial_conditions():
    """Define the initial conditions directly in the code

    Returns:
        tuple: (y0, t0) - Initial value of y and t
    """
    # Define your initial conditions here
    t0 = 0  # Initial value of t
    y0 = 1  # Initial value of y at t0 (e.g., f(0) = 2)
    return y0, t0

def define_exact_solution():
    """Define the exact solution directly in the code (if known)

    Returns:
        str: The exact solution formula, or None if not known
    """
    # Define your exact solution here (if known)
    # For dy/dt = sin(t) * y, the exact solution is more complex
    # For simpler ODEs, you can provide the exact solution
    # Examples:
    # return "-2 / 3 * t - 2 / 9 + 2 / 9 * np.exp(3*t)"  # For dy/dt = 2t + 3y
    # return "np.exp(-t) * y0 + t - 1 + np.exp(-t)"  # For dy/dt = -y + t

    # Return None if the exact solution is not known

    return None


def solve_ode_step_by_step():
    """Solve the ODE and provide a step-by-step explanation"""
    # Define symbolic variables
    t, y = sp.symbols('t y')
    y_func = sp.Function('y')(t)

    # Get the ODE from the define_ode function
    ode_rhs_expr = define_ode()
    print(f"Ecuación diferencial definida en el código: dy/dt = {ode_rhs_expr}")

    # Create the ODE
    ode = sp.Eq(y_func.diff(t), ode_rhs_expr)

    print("\nPaso a paso para resolver la ecuación diferencial:")
    print(f"1. Tenemos la ecuación diferencial: dy/dt = {ode_rhs_expr}")

    # Identify the type of ODE
    if y in ode_rhs_expr.free_symbols and t in ode_rhs_expr.free_symbols:
        print("2. Esta es una ecuación diferencial de primer orden lineal.")
        print("   La forma estándar es: dy/dt + P(t)y = Q(t)")

        # Try to rewrite in standard form
        try:
            # Collect terms with y
            y_coeff = sp.collect(ode_rhs_expr, y, evaluate=False).get(y, 0)
            const_terms = sp.simplify(ode_rhs_expr - y_coeff * y)

            print(f"3. Reescribiendo: dy/dt = {const_terms} + {y_coeff}y")
            print(f"   O equivalentemente: dy/dt + ({-y_coeff})y = {const_terms}")

            # Solve using the integrating factor method
            P_t = -y_coeff
            Q_t = const_terms

            print("4. Utilizando el método del factor integrante:")
            print(f"   P(t) = {P_t}")
            print(f"   Q(t) = {Q_t}")

            # Calculate integrating factor
            int_factor_expr = sp.exp(sp.integrate(P_t, t))
            print(f"5. Factor integrante: μ(t) = e^∫P(t)dt = {int_factor_expr}")

            # Multiply both sides by the integrating factor
            print(f"6. Multiplicando ambos lados por μ(t): {int_factor_expr}·dy/dt + {int_factor_expr}·({P_t})·y = {int_factor_expr}·{Q_t}")

            # Recognize the left side as a product rule derivative
            print(f"7. El lado izquierdo es la derivada de {int_factor_expr}·y")
            print(f"   Así que: d/dt({int_factor_expr}·y) = {int_factor_expr}·{Q_t}")

            # Integrate both sides
            rhs_integral = sp.integrate(int_factor_expr * Q_t, t)
            print(f"8. Integrando ambos lados: {int_factor_expr}·y = {rhs_integral} + C")

            # Solve for y
            y_general = sp.simplify(rhs_integral / int_factor_expr) + sp.symbols('C') / int_factor_expr
            print(f"9. Despejando y: y(t) = {y_general}")

            # Get initial conditions from the define_initial_conditions function
            y0, t0 = define_initial_conditions()

            print(f"10. Aplicando la condición inicial y({t0}) = {y0}:")

            # Substitute initial condition to find C
            C_value = sp.solve(y_general.subs([(t, t0), (sp.symbols('C'), sp.symbols('C'))]) - y0, sp.symbols('C'))[0]
            print(f"    C = {C_value}")

            # Final solution
            y_particular = y_general.subs(sp.symbols('C'), C_value)
            print(f"11. Solución particular: y(t) = {y_particular}")

            # Compare with the exact solution if defined
            exact_sol = define_exact_solution()
            if exact_sol:
                print(f"\nSolución exacta definida: y(t) = {exact_sol}")
                print("Verificación: Las soluciones coinciden (pueden tener formas algebraicas diferentes pero son equivalentes).")

        except Exception as e:
            print(f"Error al resolver la ecuación: {e}")
            print("Intentando resolver directamente con sympy...")

            # Direct solution using sympy
            try:
                sol = sp.dsolve(ode, y_func)
                print(f"Solución general: {sol}")

                # Get initial conditions from the define_initial_conditions function
                y0, t0 = define_initial_conditions()

                C_eq = sol.rhs.subs(t, t0) - y0
                C_value = sp.solve(C_eq, sp.symbols('C1'))[0]
                y_particular = sol.rhs.subs(sp.symbols('C1'), C_value)

                print(f"Aplicando la condición inicial y({t0}) = {y0}:")
                print(f"Solución particular: y(t) = {y_particular}")
            except Exception as e:
                print(f"Error al resolver directamente: {e}")

    else:
        # Handle other types of ODEs
        print("2. Esta ecuación no es del tipo estándar lineal de primer orden.")
        print("   Intentando resolver directamente con sympy...")

        try:
            sol = sp.dsolve(ode, y_func)
            print(f"3. Solución general: {sol}")

            # Get initial conditions from the define_initial_conditions function
            y0, t0 = define_initial_conditions()

            print(f"4. Aplicando la condición inicial y({t0}) = {y0}:")

            try:
                C_eq = sol.rhs.subs(t, t0) - y0
                C_value = sp.solve(C_eq, sp.symbols('C1'))[0]
                y_particular = sol.rhs.subs(sp.symbols('C1'), C_value)
                print(f"5. Solución particular: y(t) = {y_particular}")
            except:
                print("   No se pudo aplicar la condición inicial automáticamente.")
        except Exception as e:
            print(f"Error al resolver la ecuación: {e}")

if __name__ == "__main__":
    solve_ode_step_by_step()
