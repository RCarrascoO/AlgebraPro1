import sympy as sp

def calcular_intersecciones(expr, x):
    intersecciones_x = []
    interseccion_y = None
    try:
        raices = sp.solve(expr, x)
        intersecciones_x = [float(r) for r in raices if r.is_real]
        interseccion_y = float(expr.subs(x, 0))
        print(f"Justificación: Raíces f(x)=0: {raices}, intersección y: f(0)={expr.subs(x,0)}")
    except:
        print("Error en el cálculo de intersecciones.")
    return intersecciones_x, interseccion_y