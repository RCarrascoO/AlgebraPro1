from typing import Iterable, List, Optional, Tuple
import sympy as sp
from sympy import lambdify
import matplotlib.pyplot as plt

def _linspace(a: float, b: float, n: int) -> List[float]:
    if n <= 1:
        return [a]
    paso = (b - a) / float(n - 1)
    return [a + i * paso for i in range(n)]


def graficar_funcion(
    expr: sp.Expr,
    x: sp.Symbol,
    intersecciones_x: Iterable[float],
    interseccion_y: Optional[float],
    punto_evaluado: Optional[Tuple[float, float]] = None,
    dominio: str = "Todo R",
) -> None:
    # Generar puntos sin NumPy para un trazado suave
    valores_x = _linspace(-10.0, 10.0, 400)
    # Crear función numérica (usa math internamente)
    f_num = lambdify(x, expr, modules=["math"])
    valores_y = []
    for xv in valores_x:
        try:
            yv = f_num(xv)
            # Si devuelve complejo o no convertible, marcamos como NaN
            if isinstance(yv, complex):
                valores_y.append(float('nan'))
            else:
                valores_y.append(float(yv))
        except Exception:
            # Discontinuidades/división por cero, etc.
            valores_y.append(float('nan'))
    
    plt.figure(figsize=(8,6))
    plt.plot(valores_x, valores_y, label='f(x)', color='blue')
    
    if intersecciones_x:
        plt.scatter(intersecciones_x, [0]*len(intersecciones_x), color='green', label='Intersecciones con X', zorder=5)
    if interseccion_y is not None:
        plt.scatter([0], [interseccion_y], color='orange', label='Intersección con Y', zorder=5)
    
    if punto_evaluado:
        plt.scatter(punto_evaluado[0], punto_evaluado[1], color='red', s=100, label='Punto evaluado', zorder=5)
    
    plt.title('Gráfica de la Función')
    plt.xlabel('x (independiente)')
    plt.ylabel('y (dependiente)')
    plt.legend()
    plt.grid(True)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.show()