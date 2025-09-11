from typing import Tuple
import sympy as sp

def evaluar_punto(expr: sp.Expr, x_val: float, x: sp.Symbol) -> Tuple[float, float]:
    """Evalúa f(x) en x_val y retorna el par (x_val, f(x_val)).

    Lanza ValueError en casos inválidos (p. ej. división por cero).
    """
    try:
        print(f"Paso 1: Sustituir x={x_val} en {expr}")
        expr_sustituida = expr.subs(x, x_val)
        print(f"Paso 2: Expresión: {expr_sustituida}")
        resultado = float(expr_sustituida.evalf())
        print(f"Paso 3: Resultado: f({x_val}) = {resultado}")
        return (x_val, resultado)
    except:
        raise ValueError("Evaluación inválida (por ejemplo, división por cero).")