from typing import Tuple
import sympy as sp
from sympy import SympifyError

def analizar_funcion(expr_str: str) -> Tuple[sp.Expr, sp.Symbol]:
    """Convierte un string de función en una expresión SymPy y devuelve (expr, x).

    Acepta racionales usando '/', por ejemplo: '(x+1)/(x-2)'.
    Lanza ValueError si la expresión no es válida.
    """
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