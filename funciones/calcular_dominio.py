from typing import Union
import sympy as sp

def calcular_dominio(expr: sp.Expr, x: sp.Symbol) -> str:
    """Calcula el dominio de una función racional/polinómica como string.

    Para polinómicas retorna 'Todo R'; para racionales excluye ceros reales
    del denominador.
    """
    dominio = "Todo R"
    try:
        num, den = sp.fraction(sp.together(expr))
        if den != 1:
            ceros = sp.solve(den, x)
            exclusiones = [str(z) for z in ceros if z.is_real]
            dominio = f"R \\ {{ {' ,'.join(exclusiones)} }}" if exclusiones else "Todo R"
            print(f"Justificación: Denominador = {den}, ceros en x = {ceros}")
        else:
            print("Justificación: Polinómica, sin restricciones.")
    except:
        dominio = "Error en el cálculo del dominio."
    return dominio