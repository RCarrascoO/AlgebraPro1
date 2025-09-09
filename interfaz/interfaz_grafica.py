import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazGrafica:
    def __init__(self,root):
        self.root = root
        self.root.title("Calculadora Simbólica")
        self.func_str = tk.StringVar()
        self.x_value = tk.DoubleVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="ingrese la función (f(x))").pack()
        tk.Entry(self.root, textvariable=self.func_str, width=50 ).pack()
        tk.Label(self.root, text="ingrese el valor de x").pack()
        tk.Entry(self.root,textvariable=self.x_value, width=50).pack()
        tk.Button(self.root, text="analizar función", command=self.analizar_funcion).pack()
        tk.Button(self.root, text="graficar función", command=self.grafciar_funcion).pack()
        



root = tk.Tk()
app = InterfazGrafica(root)
root.mainloop()
