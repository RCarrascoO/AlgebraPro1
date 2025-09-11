import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, Interval, solveset, S, oo, sympify


class InterfazGrafica:
    def __init__(self,root):
        # Inicializa la ventana principal y las variables de la interfaz
        self.root = root
        self.root.title("Calculadora Simbólica")
        self.funcion_str = tk.StringVar()
        self.valor_x = tk.DoubleVar()
        self.crear_interfaz()

    def crear_interfaz(self):
        # Crea los elementos gráficos de la interfaz
        tk.Label(self.root, text="ingrese la función (f(x))").pack()
        tk.Entry(self.root, textvariable=self.funcion_str, width=50 ).pack()

        tk.Label(self.root, text="ingrese el valor de x").pack()
        tk.Entry(self.root,textvariable=self.valor_x, width=50).pack()

        tk.Button(self.root, text="analizar función", command=self.analizar_funcion).pack()
        tk.Button(self.root, text="graficar función", command=self.graficar_funcion).pack()

    def analizar_funcion(self):
        # Toma la función ingresada
        funcion_texto = self.funcion_str.get()

        try:
            x = sp.symbols('x')
            funcion = sp.sympify(funcion_texto)

            dominio = self.calcular_dominio(funcion)
            recorrido = self.calcular_recorrido(funcion, dominio)

            intersecciones_x = self.calcular_intersecciones_x(funcion)
            interseccion_y = self.calcular_intersecciones_y(funcion)

            evaluacion = None
            if self.valor_x.get():
                evaluacion = self.evaluar_en_punto(funcion, self.valor_x.get())

            self.mostrar_resultados(dominio, recorrido, intersecciones_x, interseccion_y, evaluacion)
        
        except Exception as e:
            messagebox.showerror("Error", f" ocurrió un error al analizar la función: {e}")

    def calcular_dominio(self, funcion):
        # Determina el dominio de la función
        x = sp.symbols('x')
        try:
            dominio = sp.calculus.util.function_domain(funcion, x)
        except:
            dominio = Interval(-oo, oo)
        return dominio

    def calcular_recorrido(self, funcion, dominio):
        # Calcula un rango aproximado de valores de la función en el dominio
        x_inicio = int(dominio.start) if dominio.start.is_finite else -10
        x_fin = int(dominio.end) if dominio.end.is_finite else 10
        rango_valores = [funcion.subs('x', i) for i in range (x_inicio, x_fin + 1)]
        return rango_valores

    def calcular_intersecciones_x(self, funcion):
        # Busca los puntos donde la función cruza el eje x
        x = sp.symbols('x')
        intersecciones = sp.solveset(funcion, x, domain=sp.S.Reals)
        return intersecciones
    
    def calcular_intersecciones_y(self, funcion):
        # Calcula el valor de la función cuando x es 0
        return funcion.subs('x',0)
    
    def evaluar_en_punto(self, funcion, x_valor):
        # Evalúa la función en un punto específico
        return funcion.subs('x', x_valor)

    def mostrar_resultados(self, dominio, recorrido, intersecciones_x, interseccion_y, evaluacion):
        # Muestra los resultados del análisis
        resultado = f"dominio: {dominio}\n"
        resultado += f"recorrido aproximado: {recorrido}\n"
        resultado += f"intersecciones con el eje x: {intersecciones_x}\n"
        resultado += f"interseccion con el eje y: {interseccion_y}\n"

        if evaluacion is not None:
            resultado += f"evaluacion en x={self.valor_x.get()}: f(x) = {evaluacion}\n"
        messagebox.showinfo("Resultados del análisis", resultado)

    def graficar_funcion(self):
        # Genera y muestra la gráfica de la función 
        funcion_texto = self.funcion_str.get()
        
        try:
            x = sp.symbols('x')
            funcion = sp.sympify(funcion_texto)
            
            # Generar valores de x para graficar
            x_vals = list(range(-10, 11))
            y_vals = [funcion.subs('x', val) for val in x_vals]
            
            fig, ax = plt.subplots(figsize=(6,6))
            ax.plot(x_vals, y_vals, label=f"f(x) = {funcion_texto}")
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            
            if self.valor_x.get():
                y_eval = funcion.subs('x', self.valor_x.get())
                ax.scatter(self.valor_x.get(), y_eval, color='red', label=f"Punto evaluado: ({self.valor_x.get()}, {y_eval})")
            
            ax.set_title(f"Gráfica de f(x) = {funcion_texto}")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()
            
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.get_tk_widget().pack()
            canvas.draw()
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al graficar la función: {e}")




#inicio de la aplicación
root = tk.Tk()
app = InterfazGrafica(root)
root.mainloop()
