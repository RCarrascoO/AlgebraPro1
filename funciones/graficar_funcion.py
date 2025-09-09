import sympy as sp
import matplotlib.pyplot as plt

def graficar_funcion(expr, x, intersecciones_x, interseccion_y, punto_evaluado=None, dominio="Todo R"):
    valores_x = sp.linspace(-10, 10, 400)
    valores_y = [expr.subs(x, xv) for xv in valores_x]
    
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