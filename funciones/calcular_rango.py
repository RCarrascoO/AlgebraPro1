from typing import Union
import sympy as sp

def calcular_rango(expr: sp.Expr, x: sp.Symbol) -> str:
    """Devuelve un rango aproximado como string usando límites en ±∞.

    Si los límites coinciden sugiere un intervalo; en otros casos devuelve
    un mensaje indicando que se consulte el gráfico.
    """
    rango_aprox = "Difícil simbólicamente; ver gráfico."
    try:
        lim_inf = sp.limit(expr, x, float('-inf'))
        lim_sup = sp.limit(expr, x, float('inf'))
        print(f"Justificación: Límite x→-∞: {lim_inf}, x→∞: {lim_sup}")
        if lim_inf == lim_sup:
            rango_aprox = f"[{lim_inf}, {lim_sup}]"  # Asintota horizontal simple
    except:
        pass
    return rango_aprox