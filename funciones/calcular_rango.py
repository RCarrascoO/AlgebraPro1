import sympy as sp

def calcular_rango(expr, x):
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