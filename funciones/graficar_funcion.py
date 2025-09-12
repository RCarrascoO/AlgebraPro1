from typing import Iterable, List, Optional, Tuple
import math
import sympy as sp
from sympy import lambdify
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

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
    ax: Optional[Axes] = None,
    show: bool = True,
) -> None:
    """
    Dibuja la función en un Axes dado o crea uno nuevo si no se proporciona.

    - Si se pasa `ax`, no realiza plt.show() y solo dibuja sobre ese Axes.
    - Si no se pasa `ax`, crea una figura/axes y muestra la ventana si `show` es True.
    """
    # Generar puntos sin NumPy para un trazado suave
    valores_x = _linspace(-10.0, 10.0, 400)
    paso_x = valores_x[1] - valores_x[0] if len(valores_x) > 1 else 0.05
    # Crear función numérica (usa math internamente)
    f_num = lambdify(x, expr, modules=["math"])
    # Detectar posibles singularidades (ceros reales del denominador)
    singularidades: List[float] = []
    try:
        num, den = sp.fraction(sp.together(expr))
        if den != 1:
            sols = sp.solve(sp.Eq(den, 0), x)
            singularidades = [float(s) for s in sols if s.is_real]
    except Exception:
        singularidades = []

    delta = 2 * paso_x  # vecindad para romper la línea cerca de asintotas
    y_clip = 1e6  # valores excesivos los tratamos como discontinuidad

    valores_y: List[float] = []
    for xv in valores_x:
        # Si estamos muy cerca de una singularidad, cortamos la línea
        if any(abs(xv - s) < delta for s in singularidades):
            valores_y.append(float('nan'))
            continue
        try:
            yv = f_num(xv)
            # complejo, no finito o excesivo => NaN para cortar segmento
            if isinstance(yv, complex) or not isinstance(yv, (int, float)):
                valores_y.append(float('nan'))
            elif not math.isfinite(yv) or abs(yv) > y_clip:
                valores_y.append(float('nan'))
            else:
                valores_y.append(float(yv))
        except Exception:
            valores_y.append(float('nan'))

    # Romper segmentos con saltos bruscos entre puntos consecutivos
    for i in range(1, len(valores_y)):
        y0, y1 = valores_y[i - 1], valores_y[i]
        if not (math.isfinite(y0) and math.isfinite(y1)):
            continue
        if abs(y1 - y0) > 50 * max(1.0, abs(y0)):
            valores_y[i] = float('nan')
    
    # Preparar Axes
    own_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        own_fig = True
    else:
        fig = ax.figure
    ax.clear()

    # Trazar
    ax.plot(valores_x, valores_y, label='f(x)', color='blue')
    
    if intersecciones_x:
        ax.scatter(intersecciones_x, [0]*len(intersecciones_x), color='green', label='Intersecciones con X', zorder=5)
    if interseccion_y is not None:
        ax.scatter([0], [interseccion_y], color='orange', label='Intersección con Y', zorder=5)
    
    if punto_evaluado:
        ax.scatter(
            punto_evaluado[0],
            punto_evaluado[1],
            color='red',
            s=36,  # tamaño más pequeño para mayor precisión visual
            label='Punto evaluado',
            zorder=5,
        )
        # Anotar coordenadas (x, y) cerca del punto evaluado
        try:
            px = float(punto_evaluado[0])
            py = float(punto_evaluado[1])
            ax.annotate(
                f"({px:.4g}, {py:.4g})",
                xy=(px, py),
                xytext=(6, 6),
                textcoords='offset points',
                fontsize=8,
                color='red',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='red', alpha=0.6),
            )
        except Exception:
            pass
    
    ax.set_title('Gráfica de la Función')
    ax.set_xlabel('x (independiente)')
    ax.set_ylabel('y (dependiente)')
    ax.legend()
    ax.grid(True)
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)

    # Mostrar solo si creamos la figura aquí y se solicitó
    if own_fig and show:
        plt.show()