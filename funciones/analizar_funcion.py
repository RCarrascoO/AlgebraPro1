import sympy as sp
from sympy import SympifyError

def analizar_funcion(expr_str):
    x = sp.symbols('x')
    try:
        if '/' in expr_str:
            num, den = expr_str.split('/', 1)
            num = sp.sympify(num)
            den = sp.sympify(den)
            expr = num / den
        else:
            expr = sp.sympify(expr_str)
        return expr, x
    except SympifyError:
        raise ValueError("Función inválida. Usa un formato como 'x**2 + 1' o '(x+1)/(x-2)'.")