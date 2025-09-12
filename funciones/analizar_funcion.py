from typing import Tuple
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)


def analizar_funcion(expr_str: str) -> Tuple[sp.Expr, sp.Symbol]:
    """Convierte un string de función en una expresión SymPy y devuelve (expr, x).

    Soporta de manera amigable:
    - Multiplicación implícita: 2x -> 2*x, (x+1)(x-2) -> (x+1)*(x-2)
    - Potencia con caret: x^2 -> x**2
    - Constantes y funciones: pi, e, sin, cos, tan, exp, log, etc.
    """
    x = sp.symbols("x")
    s = (expr_str or "").strip()
    if not s:
        raise ValueError(
            "Función vacía. Ingresa una expresión en x, por ejemplo: x**2 - 2x + 1"
        )

    # Aceptar ^ como operador de potencia
    s = s.replace("^", "**")

    transformations = standard_transformations + (implicit_multiplication_application,)
    local_dict = {
        "x": x,
        # constantes
        "pi": sp.pi,
        "e": sp.E,
        # funciones comunes
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "exp": sp.exp,
        "log": sp.log,
        "sqrt": sp.sqrt,
    }
    try:
        expr = parse_expr(s, transformations=transformations, local_dict=local_dict, evaluate=True)
        expr = sp.simplify(expr)
        # Validar que solo use la variable x
        otros = {str(sym) for sym in expr.free_symbols if sym != x}
        if otros:
            raise ValueError(
                f"Solo se admite la variable x. Encontrado(s): {', '.join(sorted(otros))}"
            )
        return expr, x
    except Exception as exc:
        raise ValueError(
            "Función inválida. Ejemplos válidos: x**2 - 2x + 1, (x+1)/(x-2), sin(x)+2. (Aceptamos x^2 por conveniencia)"
        ) from exc