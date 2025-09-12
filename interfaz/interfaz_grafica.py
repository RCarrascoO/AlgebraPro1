import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import io
import contextlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Lógica reutilizable
from funciones.analizar_funcion import analizar_funcion as parsear_funcion
from funciones.calcular_dominio import calcular_dominio
from funciones.calcular_rango import calcular_rango
from funciones.calcular_intersecciones import calcular_intersecciones
from funciones.evaluar_punto import evaluar_punto
from funciones.graficar_funcion import graficar_funcion as graficar_externa


class InterfazGrafica:
    def __init__(self, root):
        # Inicializa la ventana principal y las variables de la interfaz
        self.root = root
        self.root.title("Calculadora Simbólica")
        self.funcion_str = tk.StringVar()
        self.valor_x_str = tk.StringVar()
        self.crear_interfaz()

    def crear_interfaz(self):
        # Crea los elementos gráficos de la interfaz
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Contenedor con separador redimensionable (izquierda/derecha)
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief="raised")
        paned.pack(padx=10, pady=10, fill="both", expand=True)

        # Panel izquierdo y derecho
        left = ctk.CTkFrame(paned)
        right = ctk.CTkFrame(paned)
        paned.add(left, minsize=260)
        paned.add(right, minsize=300)

        # Posición inicial 40% / 60% (una sola vez cuando tenga tamaño)
        self._sash_initialized = False
        def _init_sash(event):
            if not self._sash_initialized:
                w = paned.winfo_width() or event.width
                if w and w > 0:
                    paned.sash_place(0, int(w * 0.4), 0)
                    self._sash_initialized = True
        paned.bind("<Configure>", _init_sash)

        # Controles e información (izquierda)
        ctk.CTkLabel(left, text="Ingrese la función f(x)").pack(anchor="w")
        ctk.CTkEntry(left, textvariable=self.funcion_str, width=420).pack(fill="x", pady=(2, 8))

        ctk.CTkLabel(left, text="Ingrese el valor de x (opcional)").pack(anchor="w")
        ctk.CTkEntry(left, textvariable=self.valor_x_str, width=200).pack(pady=(2, 8))

        btns = ctk.CTkFrame(left)
        btns.pack(pady=4, fill="x")
        ctk.CTkButton(btns, text="Analizar función", command=self.analizar_funcion).pack(
            side="left", padx=(0, 8)
        )
        ctk.CTkButton(btns, text="Graficar función", command=self.graficar_funcion).pack(
            side="left"
        )

        # Panel de resultados/justificación
        self.texto_resultados = ctk.CTkTextbox(left, height=200, width=560)
        self.texto_resultados.pack(pady=6, fill="both", expand=True)

        # Gráfico embebido (derecha)
        self.plot_frame = ctk.CTkFrame(right)
        self.plot_frame.pack(fill="both", expand=True)
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Gráfica de la Función")
        self.ax.set_xlabel("x (independiente)")
        self.ax.set_ylabel("y (dependiente)")
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

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
                messagebox.showwarning(
                    "Validación",
                    f"Solo se admite la variable x. Encontrado(s): {', '.join(sorted(otros))}",
                )
                return

            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                # Cálculos usando módulos reutilizables
                dominio = calcular_dominio(expr, x)
                rango = calcular_rango(expr, x)
                intersecciones_x, interseccion_y = calcular_intersecciones(expr, x)

                evaluacion = None
                val_text = self.valor_x_str.get().strip()
                if val_text != "":
                    try:
                        x_val_float = float(val_text)
                        _, y_eval = evaluar_punto(expr, x_val_float, x)
                        evaluacion = y_eval
                    except Exception as eval_err:
                        evaluacion = f"Error al evaluar: {eval_err}"

            justificacion = buffer.getvalue()
            self.mostrar_resultados(
                dominio, rango, intersecciones_x, interseccion_y, evaluacion, justificacion
            )
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al analizar la función: {e}")

    def mostrar_resultados(
        self,
        dominio,
        rango,
        intersecciones_x,
        interseccion_y,
        evaluacion,
        justificacion: str = "",
    ):
        # Muestra los resultados del análisis
        resultado = f"dominio: {dominio}\n"
        resultado += f"rango aproximado: {rango}\n"
        resultado += f"intersecciones con el eje x: {intersecciones_x}\n"
        resultado += f"interseccion con el eje y: {interseccion_y}\n"

        if evaluacion is not None:
            resultado += f"evaluacion en x={self.valor_x_str.get()}: f(x) = {evaluacion}\n"
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
            val_text = self.valor_x_str.get().strip()
            if val_text != "":
                try:
                    x_val = float(val_text)
                    x_val, y_val = evaluar_punto(expr, x_val, x)
                    punto = (x_val, y_val)
                except Exception:
                    punto = None
            dom = calcular_dominio(expr, x)
            # Dibuja en el Axes embebido y refresca canvas
            graficar_externa(
                expr,
                x,
                intersecciones_x,
                interseccion_y,
                punto_evaluado=punto,
                dominio=dom,
                ax=self.ax,
                show=False,
            )
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al graficar la función: {e}")


