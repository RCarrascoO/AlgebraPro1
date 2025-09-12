from typing import Union
import sympy as sp
from sympy import S
from sympy.calculus.util import function_range


def _fmt_val(v: sp.Expr) -> str:
    """Formatea valores de SymPy a una cadena amigable.
    - AccumBounds(a,b) -> "[a, b] (oscilatorio)"
    - oo/-oo -> "∞"/"-∞"
    - Números -> con 6 cifras significativas
    - Otros -> str(v)
    """
    if v is sp.oo:
        return "∞"
    if v is -sp.oo:
        return "-∞"
    if isinstance(v, sp.AccumBounds):
        a = sp.N(v.min)
        b = sp.N(v.max)
        return f"[{a}, {b}] (oscilatorio)"
    if isinstance(v, (sp.Integer, sp.Rational, sp.Float)):
        return str(sp.N(v, 6))
    return str(v)


def _fmt_interval_like(obj: sp.Expr) -> str:
    """Formatea Interval/AccumBounds/conjuntos comunes a texto legible."""
    if isinstance(obj, sp.Interval):
        a = _fmt_val(obj.start)
        b = _fmt_val(obj.end)
        lb = "[" if obj.left_open is False else "("
        rb = "]" if obj.right_open is False else ")"
        return f"{lb}{a}, {b}{rb}"
    if isinstance(obj, sp.AccumBounds):
        a = _fmt_val(obj.min)
        b = _fmt_val(obj.max)
        # quitar el sufijo (oscilatorio) aquí para integrarlo en intervalo
        a = a.replace(" (oscilatorio)", "")
        b = b.replace(" (oscilatorio)", "")
        return f"[{a}, {b}]"
    if obj == S.Reals:
        return "Todo R"
    return str(obj)


def calcular_rango(expr: sp.Expr, x: sp.Symbol) -> str:
    """Devuelve un rango preferentemente simbólico y legible para humanos.

    Intenta primero function_range; si falla, usa límites en ±∞ con
    formateo amigable (evita mostrar AccumBounds crudo).
    """
    # 1) Intento simbólico
    try:
        rset = function_range(expr, x, S.Reals)
        friendly = _fmt_interval_like(rset)
        print(f"Justificación: Rango (simbólico): {friendly}")
        return friendly
    except Exception:
        pass

    # 2) Aproximación por límites
    rango_aprox = "Difícil simbólicamente; ver gráfico."
    try:
        lim_inf = sp.limit(expr, x, -sp.oo)
        lim_sup = sp.limit(expr, x, sp.oo)
        finf = _fmt_val(lim_inf)
        fsup = _fmt_val(lim_sup)
        print(f"Justificación: Límites — x→-∞: {finf}, x→∞: {fsup}")
        if lim_inf == lim_sup:
            # si ambos son iguales (incluye AccumBounds), formatear intervalo
            if isinstance(lim_inf, sp.AccumBounds):
                rango_aprox = _fmt_interval_like(lim_inf)
            else:
                rango_aprox = f"[{_fmt_val(lim_inf)}, {_fmt_val(lim_sup)}]"
    except Exception:
        pass
    return rango_aprox