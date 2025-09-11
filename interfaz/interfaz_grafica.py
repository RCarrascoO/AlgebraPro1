import tkinter as tk
from tkinter import messagebox
import io
import contextlib

# Lógica reutilizable
from funciones.analizar_funcion import analizar_funcion as parsear_funcion
from funciones.calcular_dominio import calcular_dominio
from funciones.calcular_rango import calcular_rango
from funciones.calcular_intersecciones import calcular_intersecciones
from funciones.evaluar_punto import evaluar_punto
from funciones.graficar_funcion import graficar_funcion as graficar_externa


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
        tk.Entry(self.root, textvariable=self.funcion_str, width=50).pack()

        tk.Label(self.root, text="ingrese el valor de x").pack()
        tk.Entry(self.root, textvariable=self.valor_x, width=50).pack()

        tk.Button(self.root, text="analizar función", command=self.analizar_funcion).pack()
        tk.Button(self.root, text="graficar función", command=self.graficar_funcion).pack()

        # Panel de resultados/justificación
        self.texto_resultados = tk.Text(self.root, height=12, width=60)
        self.texto_resultados.pack(pady=6)

    def analizar_funcion(self):
        # Toma la función ingresada
        funcion_texto = self.funcion_str.get().strip()
        if not funcion_texto:
            messagebox.showwarning("Validación", "Ingrese una función en x, por ejemplo: x**2 - 4")
            return

        try:
            # Parseo y símbolos
            expr, x = parsear_funcion(funcion_texto)
            # Validación: solo variable x
            otros = {str(s) for s in expr.free_symbols if s != x}
            if otros:
                messagebox.showwarning("Validación", f"Solo se admite la variable x. Encontrado(s): {', '.join(sorted(otros))}")
                return

            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                # Cálculos usando módulos reutilizables
                dominio = calcular_dominio(expr, x)
                rango = calcular_rango(expr, x)
                intersecciones_x, interseccion_y = calcular_intersecciones(expr, x)

                evaluacion = None
                if self.valor_x.get():
                    try:
                        _, y_eval = evaluar_punto(expr, self.valor_x.get(), x)
                        evaluacion = y_eval
                    except Exception as eval_err:
                        evaluacion = f"Error al evaluar: {eval_err}"

            justificacion = buffer.getvalue()
            self.mostrar_resultados(dominio, rango, intersecciones_x, interseccion_y, evaluacion, justificacion)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al analizar la función: {e}")


    def mostrar_resultados(self, dominio, rango, intersecciones_x, interseccion_y, evaluacion, justificacion: str = ""):
        # Muestra los resultados del análisis
        resultado = f"dominio: {dominio}\n"
        resultado += f"rango aproximado: {rango}\n"
        resultado += f"intersecciones con el eje x: {intersecciones_x}\n"
        resultado += f"interseccion con el eje y: {interseccion_y}\n"

        if evaluacion is not None:
            resultado += f"evaluacion en x={self.valor_x.get()}: f(x) = {evaluacion}\n"
        if justificacion:
            resultado += "\n--- Justificación (cálculo) ---\n" + justificacion
        # Mostrar en panel
        self.texto_resultados.delete("1.0", tk.END)
        self.texto_resultados.insert(tk.END, resultado)

    def graficar_funcion(self):
        # Genera la gráfica usando el módulo reutilizable (abre ventana de Matplotlib)
        funcion_texto = self.funcion_str.get().strip()
        if not funcion_texto:
            messagebox.showwarning("Validación", "Ingrese una función en x, por ejemplo: x**2 - 4")
            return
        try:
            expr, x = parsear_funcion(funcion_texto)
            intersecciones_x, interseccion_y = calcular_intersecciones(expr, x)
            punto = None
            if self.valor_x.get():
                try:
                    x_val, y_val = evaluar_punto(expr, self.valor_x.get(), x)
                    punto = (x_val, y_val)
                except Exception:
                    punto = None
            dom = calcular_dominio(expr, x)
            graficar_externa(expr, x, intersecciones_x, interseccion_y, punto_evaluado=punto, dominio=dom)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al graficar la función: {e}")


