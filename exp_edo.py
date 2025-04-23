import sympy as sp
from sympy import symbols, Eq, dsolve, Function

'''
ecuacion diferencial:
1. juntar mismas variables a lados distintos x=y
2. integrar ambos lados
3. elevo cada lado sobre e
4. despejar y -- 
5. reemplazar los puntos iniciales para obtener c
6. reemplazar c
'''

x = symbols('x')
f = Function('f')

ode = Eq(f(x).diff(x), x * f(x))
sol = dsolve(ode, f(x), ics={f(1): 1})

print(sol)